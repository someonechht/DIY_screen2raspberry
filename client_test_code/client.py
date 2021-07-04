# importing the required packages
from os import wait
import pyautogui
import numpy as np
import cv2
import socket
import screencapture

# Specify resolution
resolution = pyautogui.size()

print("you are the client")
ip = input("server ip: ")

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, 1024))


# np.array(pyautogui.screenshot())
server.send(bytes(str(resolution.width), 'utf8'))
pyautogui.sleep(0.5)
server.send(bytes(str(resolution.height), 'utf8'))

image = screencapture.capture_screenshot()
print(len(image))
server.send(image)

server.close()