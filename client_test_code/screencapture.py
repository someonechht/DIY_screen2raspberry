# importing the required packages
import pyautogui
import numpy as np
import cv2
import socket

# Specify resolution
resolution = pyautogui.size()

print("you are the client")
ip = "192.168.10.166"# input("server ip: ")

# Create socket
client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_server.connect((ip, 1024))


# np.array(pyautogui.screenshot())
while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bytesize = frame.nbytes
        #client_server.send(bytearray(bytesize))
        client_server.send(frame)
