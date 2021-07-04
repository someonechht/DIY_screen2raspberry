# importing the required packages
from os import wait
from numpy.lib.type_check import imag
import pyautogui
import numpy as np
import cv2
import socket
from mss import mss
from PIL import Image





def capture_screenshot():
    # Capture entire screen
	with mss() as sct:
		image = sct.grab(sct.monitors[1])
		return image.bgra

#img.show()
