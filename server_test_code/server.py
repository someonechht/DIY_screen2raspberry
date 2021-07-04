import pyautogui
import cv2
import numpy as np
import socket
from PIL import Image
from io import BytesIO



def client_thread(client_socket):
	width = int(client_socket.recv(1024))
	height = int(client_socket.recv(1024))
	data = bytearray()
	while len(data) < width*height*4:
		data += client_socket.recv(width*height*4)
		if not data:
			break
		print(len(data))
	img = Image.frombytes("RGB", (width, height), bytes(data), "raw", "BGRX")
	img.show()

	
	
ip = socket.gethostbyname(socket.gethostname()) #'192.168.10.214' #socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, 1024))
server_socket.listen(1) #listen to 1 client
print(ip)
while True:
	( client_socket, address ) = server_socket.accept()
	ct = client_thread(client_socket)
	if(ct != None):
		ct.run()
	
