import pyautogui
import cv2
import numpy as np
import socket
from PIL import Image
from io import BytesIO

def client_thread(client_socket):
	bytesize = 6220800
	run = True
	stream = BytesIO()
#	client_socket.recvmsg_into(bytesize)
	while run:
		data = bytearray(bytesize)
		client_socket.recvmsg_into([data])
		stream.write(data)
		
		image = Image.fromarray(data)
	#print(image)
	
	

ip = '192.168.10.166' #socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, 1024))
server_socket.listen(1)
print(ip)
while True:
	( client_socket, address ) = server_socket.accept()
	ct = client_thread(client_socket)
	ct.run()
	
