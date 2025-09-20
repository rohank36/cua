import pyautogui as ptg
import json
import logging

LOGGER = logging.getLogger(__name__)

TOOL_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "move_mouse_to",
            "description": "Move mouse to an (x,y) coordinate on the screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "int"
                    },
                    "y": {
                        "type": "int"
                    }
                },
                "required": ["x","y"],
                "additionalProperties": False
            }
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
        LOGGER.debug(f"Found {len(tool_calls)} tool call(s).")
        for call in tool_calls:
            # For function tools:
            if call.type == "function_call":
                name = call.name
                args = json.loads(call.arguments or "{}")
                LOGGER.debug("Function tool requested:", name, args)
                return True,name,args
    else:
        LOGGER.debug("No tool calls. Model returned normal assistant text.")
        return False,None,None


def move_mouse_to(x,y):
    ptg.moveTo(x,y,duration=0.0)
