from jinja2 import Template
from datetime import datetime

class Agent:
    def __init__(self, width:int, height:int):
        with open("prompt.md",encoding='utf-8') as f:
            raw_md = f.read()
        template = Template(raw_md)
        self.system_prompt = template.render(
            current_date = str(datetime.today()),
            width = width,
            height = height, 
            center_width = width//2,
            center_height = height//2,
            )
        print(self.system_prompt)


a = Agent(4,6)