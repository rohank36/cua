import pyautogui as ptg
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from llms import GPT_5_NANO
from jinja2 import Template
from datetime import datetime
import logging
import time
import uuid
from tools import TOOL_SPEC, move_mouse_to, parse_tools
import json
################################################################
load_dotenv()    
CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG) 

os.makedirs("images/", exist_ok=True) 
################################################################

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def calculate_cost(input_tokens,output_tokens,input_cost,output_cost):
    onem = 1000000
    input_cost = (input_tokens/onem) * input_cost
    completion_cost = (output_tokens/onem) * output_cost
    return input_cost + completion_cost

def llm_call(messages,model,tool_spec):
    res = CLIENT.responses.create(
        model = model.name,
        text = {"verbosity":model.verbosity}, 
        reasoning={"effort":model.reasoning},
        tools = tool_spec,
        tool_choice = "auto",
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,model.input_cost,model.output_cost)
    health = res.usage.input_tokens / model.context_window
    return res, res.output_text, cost, health

def get_system_prompt(width, height):
    with open("prompt.md",encoding='utf-8') as f:
            raw_md = f.read()
    template = Template(raw_md)
    system_prompt = template.render(
        current_date = str(datetime.today()),
        width = width,
        height = height, 
        center_width = width//2,
        center_height = height//2,
        )
    return system_prompt

def uid_hash()->str:
    return uuid.uuid4().hex
################################################################

width,height = ptg.size()
MESSAGES = [{"role":"system","content":get_system_prompt(width,height)}]   
HEALTH = 0.0
COST = 0.0

#user_request = input(">")
#user_request = user_request.strip(">").strip("")
user_request = "Move the mouse to google chrome" 
user_request_prompt = f"Generate a plan that you'll follow to complete the following task:\n{user_request}"

MESSAGES.append({"role":"user","content":user_request_prompt})
_,res_text,health,cost = llm_call(MESSAGES,GPT_5_NANO,TOOL_SPEC)
LOGGER.debug(f"{res_text}")
HEALTH = health
COST += cost
MESSAGES.append({"role":"assistant","content":f"{res_text}\nNow I will execute this plan."})

LOGGER.info("Starting...")

while True:
    if HEALTH > 0.7:
        LOGGER.info(f"System health: {HEALTH}. Terminating agent now.")
        break

    path = f"images/{uid_hash()}.png"
    ptg.screenshot(path) 
    cur_x,cur_y = ptg.position()
    base64_image = encode_image(path)
    MESSAGES.append(
        {"role":"user","content":[
                {   "type": "input_text", "text": f"The current mouse position is: ({cur_x},{cur_y})" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image}",
                }
            ]
        }
    )
    res,res_text,cost, health = llm_call(MESSAGES,GPT_5_NANO,TOOL_SPEC)
    COST += cost
    HEALTH = health
    if res_text != "": LOGGER.debug(f"Output Text:\n{res_text}")
    LOGGER.debug(f"Cost:{COST}")
    LOGGER.debug(f"Health:{HEALTH}")
    is_tool_call,name,args,call_id = parse_tools(res)

    if is_tool_call:
        result = None
        if name == "move_mouse_to":
            x = args.get("x")
            y = args.get("y")
            try:
                move_mouse_to(x, y)
                result = f"Mouse moved to ({x},{y})"
            except Exception as e:
                result = f"Error moving mouse: {e}"

        LOGGER.debug(result)

        tool_call_req_msg = {
            "type": "function_call",
            "name": name,
            "arguments": json.dumps(args or {}),
            "call_id": call_id,
        }

        tool_call_msg = {
            "type": "function_call_output",
            "name": name,
            "call_id": call_id,
            "output": result
        }

        MESSAGES.append({"role":"assistant","content":json.dumps(tool_call_req_msg)})
        MESSAGES.append({"role":"assistant","content":json.dumps(tool_call_msg)})
    else:
        LOGGER.info(res_text)
        LOGGER.info("Task completed.")
        break
    
    time.sleep(3) 

LOGGER.info("Done.")
LOGGER.info(f"Final Health: {HEALTH} | Final Cost: {COST}")
LOGGER.info(MESSAGES)



