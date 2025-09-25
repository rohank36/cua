import pyautogui as ptg
from PIL import Image, ImageDraw
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from llms import GPT_5_NANO, GPT_5_MINI
from jinja2 import Template
from datetime import datetime
import logging
import time
import uuid
from tools import TOOL_SPEC, execute_tools, parse_tools
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

def annotate_with_cursor(img_path, x, y, radius=10):
    im = Image.open(img_path).convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    # Halo
    d.ellipse((x-radius, y-radius, x+radius, y+radius), outline=(255,0,0,255), width=3)
    # Crosshair
    d.line((x-15, y, x+15, y), fill=(255,0,0,255), width=2)
    d.line((x, y-15, x, y+15), fill=(255,0,0,255), width=2)
    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(img_path)

def crop_around(img_path, x, y, box=320):
    with Image.open(img_path) as im:
        left = max(0, x - box//2); top  = max(0, y - box//2)
        right = min(im.width, left + box); bottom = min(im.height, top + box)
        crop = im.crop((left, top, right, bottom))
        crop_path = img_path.replace(".png", "_crop.png")
        crop.save(crop_path, format="PNG")
        return crop_path
################################################################

width,height = ptg.size()
MESSAGES = [{"role":"system","content":get_system_prompt(width,height)}]   
HEALTH = 0.0
COST = 0.0

user_request = "Go to https://www.youtube.com/" 
MESSAGES.append({"role":"user","content":user_request})

LOGGER.info("Starting...")
img_counter = 1
while True:
    if HEALTH > 0.7:
        LOGGER.info(f"System health: {HEALTH}. Terminating agent now.")
        break

    path = f"images/{img_counter}_{uid_hash()}.png"
    img_counter += 1
    cur_x,cur_y = ptg.position()
    ptg.screenshot(path)
    annotate_with_cursor(path,cur_x,cur_y) 
    crop_around(path,cur_x,cur_y)
    base64_image_1 = encode_image(path)
    base64_image_2 = encode_image(path.replace(".png", "_crop.png"))
    MESSAGES.append(
        {"role":"user","content":[
                {   "type": "input_text", "text": f"The current cursor position is: ({cur_x},{cur_y})" },
                {   "type": "input_text", "text": f"Here is an image of the current screen state" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image_1}",
                },
                {   "type": "input_text", "text": f"Here is a cropped image around the current cursor position to give YOU a clearer idea of where the cursor is." },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image_2}",
                },
            ]
        }
    )
    res,res_text,cost, health = llm_call(MESSAGES,GPT_5_MINI,TOOL_SPEC)
    MESSAGES.pop()
    COST += cost
    HEALTH = health
    LOGGER.debug(f"Cost:{COST}")
    LOGGER.debug(f"Health:{HEALTH}")
    is_tool_call,name,args,call_id = parse_tools(res)

    if is_tool_call:
        result = execute_tools(name,args)
        LOGGER.debug(result)
        MESSAGES.append({"role":"assistant","content":result})
        
    else:
        LOGGER.info(res_text)
        LOGGER.info("Task completed.")
        break
    
    time.sleep(3) 

LOGGER.info("Done.")
LOGGER.info(f"Final Health: {HEALTH} | Final Cost: {COST}")
LOGGER.info(MESSAGES)



