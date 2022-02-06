import numpy as np
import cv2
from mss import mss
from PIL import Image
import win32gui
import win32api

output = 'output.mp4'

opened_window = []


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        # print(hex(hwnd), title)
        if title != '':
            opened_window.append(title)


win32gui.EnumWindows(winEnumHandler, None)

windows_enum = enumerate(opened_window)
windows_dict = dict(windows_enum)
print(windows_dict)

for i in windows_dict:
    print(i, windows_dict[i])

selectStr = input()
selectNum = int(selectStr)

windowname = windows_dict[selectNum]
window_handle = win32gui.FindWindow(None, windowname)
# wDC = win32gui.GetWindowDC(window_handle)
x1, y1, x2, y2 = win32gui.GetWindowRect(window_handle)
width = abs(x1 - x2)
height = abs(y1 - y2)

mon = {'left': x1, 'top': y1, 'width': width, 'height': height}

print(mon)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))

with mss() as sct:
    while True:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(image)
        cv2.imshow('test', np.array(img))
        if cv2.waitKey(33) & 0xFF in (
            ord('q'),
            27,
        ):
            break
