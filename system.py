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

################################################################
load_dotenv()    
CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)
################################################################

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def calculate_cost(input_tokens,output_tokens,input_cost,output_cost):
    onem = 1000000
    input_cost = (input_tokens/onem) * input_cost
    completion_cost = (output_tokens/onem) * output_cost
    return input_cost + completion_cost

def llm_call(messages,model):
    res = CLIENT.responses.create(
        model = model.name,
        text = {"verbosity":model.verbosity}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,model.input_cost,model.output_cost)
    health = res.usage.input_tokens / model.context_window
    return res.output_text, cost, health

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

# TODO: think about the TOOL calls
################################################################

width,height = ptg.size()
MESSAGES = [{"role":"system","content":get_system_prompt(width,height)}]   
HEALTH = 0.0
COST = 0.0

LOGGER.info("Starting...")
while True:
    if HEALTH > 0.6:
        LOGGER.info(f"System health: {HEALTH}. Terminating agent now.")
        break
    res, cost, health = llm_call(MESSAGES)
    COST += cost
    HEALTH = health
    #MESSAGES.append({"role":"assistant","content":res}) # TODO have to think about the process here
    time.sleep(3) 

LOGGER.info("Done.")



