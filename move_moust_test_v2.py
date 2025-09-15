import time
import pyautogui

# Move to absolute position
pyautogui.moveTo(200, 200, duration=0.0)

# Move relative
pyautogui.move(100, 0, duration=0.0)

# Smooth move to target
pyautogui.moveTo(800, 500, duration=0)
