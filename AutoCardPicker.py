import subprocess
import sys
import cv2
import os
import numpy as np
import mss
import time
import pygetwindow as gw
import autoit
import requests
import keyboard

REQ_PACKAGES = [
    "opencv-python",
    "numpy",
    "mss",
    "pygetwindow",
    "pyautoit",
    "requests",
    "keyboard"
]

def Install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in REQ_PACKAGES:
    try:
        __import__(package.split('-')[0])
    except ImportError:
        print(f"Installing {package}...")
        Install(package)


def GetRobloxWindow():
    try:
        roblox_window = gw.getWindowsWithTitle('Roblox')[0]
        
        if roblox_window.isMinimized:
            return None, None
        
        if not roblox_window.isActive:
            return None, None
        
        bbox = {
            'top': roblox_window.top,
            'left': roblox_window.left,
            'width': roblox_window.width,
            'height': roblox_window.height
        }
        
        with mss.mss() as sct:
            screen = sct.grab(bbox)
            img = np.array(screen)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img, bbox

    except IndexError:
        return None, None

def MoveAndClick(x, y, bbox, small_img):
    center_x = x + small_img.shape[1] // 2
    center_y = y + small_img.shape[0] // 2

    screen_x = bbox['left'] + center_x
    screen_y = bbox['top'] + center_y

    autoit.mouse_click("left", screen_x, screen_y)

    offset_x = screen_x + small_img.shape[1] * 2  
    offset_y = screen_y + small_img.shape[0] * 2 

    autoit.mouse_move(offset_x, offset_y)

def GetCardSelection():
    available_cards = {
        '1': 'Strong',
        '2': 'Thrice',
        '3': 'Regen',
        '4': 'Revitalize'
    }
    priority_order = []
    used_numbers = set()

    print("------------------------------------------------")
    print("Choose the cards you want to be chosen in order:")
    print("1 = Strong, 2 = Thrice, 3 = Regen, 4 = Revitalize")

    for i in range(1, 5):
        while True:
            choice = input(f"{i}: ")
            if choice in available_cards and choice not in used_numbers:
                used_numbers.add(choice)
                priority_order.append(available_cards[choice])
                break
            else:
                print("Invalid choice or number already selected. Please choose again.")

    return priority_order

def GetShutdownKey():
    key = input("Enter a keybind to shut down the script (e.g., 'q', 'esc'): ")
    return key

def CountdownShutdown():
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Exiting...")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
new_folder_path = os.path.join(desktop_path, "quantum auto Curse picker")

try:
    os.makedirs(new_folder_path)
except FileExistsError:
    pass
except Exception as e:
    pass

images = {
    "Thrice.png": "https://raw.githubusercontent.com/xfarzad/quantum.wtf/refs/heads/main/Thrice.png",
    "Strong.png": "https://raw.githubusercontent.com/xfarzad/quantum.wtf/refs/heads/main/Strong.png",
    "Regen.png": "https://raw.githubusercontent.com/xfarzad/quantum.wtf/refs/heads/main/Regen.png",
    "Revitalize.png": "https://raw.githubusercontent.com/xfarzad/quantum.wtf/refs/heads/main/Revitalize.png"
}

for file_name, url in images.items():
    file_path = os.path.join(new_folder_path, file_name)

    if not os.path.exists(file_path):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.RequestException as e:
            pass

priority_order = GetCardSelection()
shutdown_key = GetShutdownKey()

image_files = [f for f in os.listdir(new_folder_path) if f.endswith('.png')]
image_paths = [(os.path.join(new_folder_path, file), file[:-4]) for file in image_files]

small_images = [(cv2.imread(path), name) for path, name in image_paths]
small_images_gray = [(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), name) for img, name in small_images]

while True:
    if keyboard.is_pressed(shutdown_key):
        os.system('cls' if os.name == 'nt' else 'clear')
        CountdownShutdown()
        break

    full_img, bbox = GetRobloxWindow()
    
    if full_img is None or bbox is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[95m")
        print("""
            ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗   ██╗    ██╗████████╗███████╗
            ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║   ██║    ██║╚══██╔══╝██╔════╝
            ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║   ██║ █╗ ██║   ██║   █████╗  
            ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║   ██║███╗██║   ██║   ██╔══╝  
            ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║██╗╚███╔███╔╝   ██║   ██║     
            ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚══╝╚══╝    ╚═╝   ╚═╝     
        """)
        print("\033[0m")
        print("Status: Paused, tab back in Roblox to continue running.")
        print(f"Exit Bind: {shutdown_key}")
        time.sleep(0.1)
        continue

    full_gray = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)

    card_found = False
    
    for name in priority_order:
        small_img = [img for img, n in small_images if n == name][0]
        small_gray = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(full_gray, small_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(result >= threshold)

        for pt in zip(*loc[::-1]):
            MoveAndClick(pt[0], pt[1], bbox, small_img)
            card_found = True
            break

        if card_found:
            break

    if not card_found:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[95m")
        print("""
            ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗   ██╗    ██╗████████╗███████╗
            ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║   ██║    ██║╚══██╔══╝██╔════╝
            ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║   ██║ █╗ ██║   ██║   █████╗  
            ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║   ██║███╗██║   ██║   ██╔══╝  
            ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║██╗╚███╔███╔╝   ██║   ██║     
            ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚══╝╚══╝    ╚═╝   ╚═╝     
        """)
        print("\033[0m")
        print("Status: Waiting for a card to appear.")
        print(f"Exit Bind: {shutdown_key}")
        time.sleep(0.1)
