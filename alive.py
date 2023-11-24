import pyautogui
import time

# Disable failsafe to prevent accidental termination of the script
pyautogui.FAILSAFE = False

def move_mouse():
    for i in range(100):
        pyautogui.moveTo(0, i * 5)
        time.sleep(0.1)  # Adjust the delay between mouse movements

def press_shift():
    for i in range(3):
        pyautogui.press('shift')
        time.sleep(0.2)  # Adjust the delay between keypresses

while True:
    time.sleep(15)  # Wait for 15 seconds
    move_mouse()
    press_shift()
