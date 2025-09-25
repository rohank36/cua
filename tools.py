import pyautogui as ptg
import json
import logging
import subprocess
import time

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG) 

TOOL_SPEC = [
    {
        "type": "function",
        "name": "move_mouse_to", 
        "description": "Move mouse to an (x,y) coordinate on the screen.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"},
                "y": {"type": "integer"}
            },
            "required": ["x", "y"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "open_google_chrome", 
        "description": "Open the google chrome web browser.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "move_mouse_and_left_click", 
        "description": "Move mouse to an (x,y) coordinate on the screen and left click.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"},
                "y": {"type": "integer"}
            },
            "required": ["x", "y"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "double_click", 
        "description": "Double click at the current mouse position.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "click", 
        "description": "Click at the current mouse position.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "go_to_website", 
        "description": "When Google Chrome is already open, go to a website specific by it's url.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
            },
            "required": ["url"],
            "additionalProperties": False
        }
    }
]

def parse_tools(res):
    tool_calls = []
    for item in res.output:
        t = getattr(item, "type", "")
        if t in ("function_call", "tool_call") or t.endswith("_call"):
            tool_calls.append(item)

    if tool_calls:
        #LOGGER.debug(f"Found {len(tool_calls)} tool call(s).")
        for call in tool_calls:
            # For function tools:
            if call.type == "function_call":
                name = call.name
                args = json.loads(call.arguments or "{}")
                call_id = getattr(call, "call_id", None) or getattr(call, "id", None)
                #LOGGER.debug(f"Function tool requested:{name},{args},call_id={call_id}")
                return True,name,args,call_id
    else:
        LOGGER.debug("No tool calls")
        return False,None,None,None
    
def execute_tools(name,args):
    tool_map = {
        "move_mouse_to": lambda a: move_mouse_to(a["x"], a["y"]),
        "move_mouse_and_left_click": lambda a: move_mouse_and_left_click(a["x"], a["y"]),
        "open_google_chrome": lambda a: open_google_chrome(),
        "double_click": lambda a: double_click(),
        "click": lambda a: click(),
        "go_to_website": lambda a: go_to_website(a["url"])
    }

    if name not in tool_map:
        msg = f"Unknown tool: {name}"
        LOGGER.error(msg)
        return msg

    result = tool_map[name](args or {})
    return result
    
def move_mouse_to(x,y):
    try:
        ptg.moveTo(x,y,duration=0.0)
        return f"Mouse moved to ({x},{y})"
    except Exception as e:
        LOGGER.error(e)
        return f"Error moving mouse: {e}"

def click():
    try:
        ptg.click()
        return f"Mouse clicked at current position"
    except Exception as e:
        LOGGER.error(e)
        return f"Error clicking"
    
def move_mouse_and_left_click(x,y):
    try:
        ptg.click(x=x,y=y,clicks=1,interval=0,button='left')
        return f"Mouse moved to ({x},{y}) and left clicked"
    except Exception as e:
        LOGGER.error(e)
        return f"Error moving mouse and left clicking: {e}"

def double_click():
    try:
        ptg.doubleClick()
        return f"Mouse double clicked"
    except Exception as e:
        LOGGER.error(e)
        return f"Error double clicking: {e}"
    
def open_google_chrome():
    try:
        chrome_x,chrome_y = ptg.center(ptg.locateOnScreen('chrome.png'))
        ptg.click(x=chrome_x, y=chrome_y, clicks=1, interval=0, button='left') 
        ptg.click(x=748,y=960,clicks=2,interval=1,button='left')
        return "Google Chrome opened"
    except Exception as e:
        LOGGER.error(e)
        return "Error opening Google Chrome"

def go_to_website(url):
    try:
        ptg.hotkey("ctrl","t")
        ptg.hotkey("ctrl","l")
        subprocess.run("clip", text=True, input=url) 
        ptg.hotkey("ctrl","v")            
        ptg.press("enter")  
        time.sleep(5)
        return f"Going to {url}"
    except Exception as e:
        LOGGER.error(e)
        return f"Error going to {url}"

