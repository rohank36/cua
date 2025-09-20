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

#ptg.moveTo(872,1067,duration=0.0)
#cur_x,cur_y = ptg.position() 
#print(cur_x,cur_y)
annotate_with_cursor("foo.png",872,1067)

#ptg.moveTo(872,1067,duration=0.0)
#time.sleep(5)
#ptg.screenshot('foo.png')

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