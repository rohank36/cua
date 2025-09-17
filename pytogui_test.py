import pyautogui as ptg

cur_mouse_pos = ptg.position() # top left corner of screen is (0,0). x increases going right, y increases going down
print(cur_mouse_pos)

cur_screen_size = ptg.size()
print(cur_screen_size)

is_mouse_on_screen:bool = ptg.onScreen(cur_mouse_pos[0],cur_mouse_pos[1])
print(is_mouse_on_screen)