import pyautogui as ptg

cur_mouse_pos = ptg.position() # top left corner of screen is (0,0). x increases going right, y increases going down
print(cur_mouse_pos)

cur_screen_size = ptg.size()
print(cur_screen_size)

is_mouse_on_screen:bool = ptg.onScreen(cur_mouse_pos[0],cur_mouse_pos[1])
print(is_mouse_on_screen)

ptg.moveTo(cur_screen_size[0]//2, cur_screen_size[1]//2, duration=0.0) # center of screen.

#ptg.click(x=737, y=994, clicks=1, interval=0, button='left') # button can be left, middle, or right.
#ptg.scroll(1000, x=737, y=994)
#ptg.typewrite('Hello world!\n', interval=0) # /n is enter.