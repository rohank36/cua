import pyautogui as ptg
import time
from PIL import Image, ImageDraw



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
    out.save(img_path)  # overwrite original

def crop_around(img_path, x, y, box=320):
    with Image.open(img_path) as im:
        left = max(0, x - box//2); top  = max(0, y - box//2)
        right = min(im.width, left + box); bottom = min(im.height, top + box)
        crop = im.crop((left, top, right, bottom))
        crop_path = img_path.replace(".png", "_crop.png")
        crop.save(crop_path, format="PNG")
        return crop_path

#chrome_location = ptg.locateOnScreen('chrome2.png')
chrome_x,chrome_y = ptg.center(ptg.locateOnScreen('chrome2.png'))
ptg.click(x=chrome_x, y=chrome_y, clicks=1, interval=0, button='left') 
ptg.click(x=748,y=960,clicks=1,interval=0,button='left')
ptg.click(x=560,y=70,duration=0)
ptg.typewrite('https://www.instacart.ca/store/\n', interval=0) # /n is enter.

#print(chrome_x,chrome_y)

#ptg.click(x=885, y=1055, clicks=1, interval=0, button='left') 
#ptg.click(x=748,y=960,clicks=1,interval=0,button='left')
#ptg.click(x=950,y=60, interval=0,button='left')

#time.sleep(3)
#ptg.click('chrome_new_tab.PNG')

#new_tab_loc = ptg.center(ptg.locateOnScreen('chrome_new_tab.PNG'))
#print(new_tab_loc)











#########################################

#ptg.screenshot('foo.png')
#annotate_with_cursor("foo.png",872,1067)
#crop_around("foo.png",872,1067)


#cur_screen_size = ptg.size()
#print(cur_screen_size)

#is_mouse_on_screen:bool = ptg.onScreen(cur_mouse_pos[0],cur_mouse_pos[1])
#print(is_mouse_on_screen)

#ptg.moveTo(cur_screen_size[0]//2, cur_screen_size[1]//2, duration=0.0) # center of screen.

# note that you can also pass None for x,y to not move the mouse anywhere.
#ptg.doubleClick()
#ptg.click(x=737, y=994, clicks=1, interval=0, button='left') # button can be left, middle, or right.
#ptg.click(button='right')  # just click
#ptg.scroll(1000, x=737, y=994)
#ptg.typewrite('Hello world!\n', interval=0) # /n is enter.

#s = ptg.password(text='', title='', default='', mask='*')
#print(s)

#ptg.screenshot('images/foo.png') 