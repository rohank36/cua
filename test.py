from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from llms import GPT_5_NANO

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def calculate_cost(input_tokens,output_tokens,input_cost,output_cost):
    onem = 1000000
    input_cost = (input_tokens/onem) * input_cost
    completion_cost = (output_tokens/onem) * output_cost
    return input_cost + completion_cost

def llm_call_nano(messages,model):
    res = client.responses.create(
        model = model.name,
        text = {"verbosity":model.verbosity}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,model.input_cost,model.output_cost)
    return res,cost


# Path to your image
image_path = "Capture.JPG"
base64_image = encode_image(image_path)

messages = [
    {"role":"user","content":[
            {   "type": "input_text", "text": "what's in this image?" },
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}",
            },
        ]
    }
]
res,cost = llm_call_nano(messages,GPT_5_NANO)
print(res)
print("\n")
print(res.output_text)
print(res.usage.input_tokens)
print(res.usage.output_tokens)
print(f"${cost}")
