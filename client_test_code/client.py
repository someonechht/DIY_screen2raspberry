# importing the required packages
import pyautogui
import numpy as np
import cv2
import socket
import screencapture
import time
import numpy as np
import win32gui
import win32ui
import mss
from PIL import Image
# Specify resolution
resolution = pyautogui.size()

print("you are the client")
ip = input("server ip: ")

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, 1024))
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

def set_pixel(img, w, x, y, rgb=(0,0,0)):
    """
    Set a pixel in a, RGB byte array
    """
    pos = (x*w + y)*3
    if pos>=len(img):return img # avoid setting pixel outside of frame
    img[pos:pos+3] = rgb
    return img

def add_mouse(img, w):
    flags, hcursor, (cx,cy) = win32gui.GetCursorInfo()
    cursor = get_cursor(hcursor)
    cursor_mean = cursor.mean(-1)
    where = np.where(cursor_mean>0)
    for x, y in zip(where[0], where[1]):
        rgb = [x for x in cursor[x,y]]
        img = set_pixel(img, w, x+cy, y+cx, rgb=rgb)
    return img


def get_cursor(hcursor):
    info = win32gui.GetCursorInfo()
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0,0), hcursor)
    
    bmpinfo = hbmp.GetInfo()
    bmpbytes = hbmp.GetBitmapBits()
    bmpstr = hbmp.GetBitmapBits(True)
    im = np.array(Image.frombuffer(
        'RGB',
         (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
         bmpstr, 'raw', 'BGRX', 0, 1))
    
    win32gui.DestroyIcon(hcursor)    
    win32gui.DeleteObject(hbmp.GetHandle())
    hdc.DeleteDC()
    return im



# np.array(pyautogui.screenshot())
server.send(bytes(str(resolution.width), 'utf8'))
pyautogui.sleep(0.25)
server.send(bytes(str(resolution.height), 'utf8'))
pyautogui.sleep(0.25)
sct = mss.mss()
while(True):
    screen = sct.monitors[0]
    img = bytearray(sct.grab(screen).rgb)
    img_with_mouse = add_mouse(img, screen['width'])
    t0 = time.time()
    server.send(img_with_mouse)
    t1 = time.time() - t0
    print("Time elapsed: ", t1)
    
sct.close()
server.close()
