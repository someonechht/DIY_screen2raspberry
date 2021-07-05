import pyautogui
import cv2
import numpy as np
import socket
from PIL import Image
from io import BytesIO
import pyglet
import threading

class server():
	def __init__(self):
		self.run = True
		self.img = None
		self.thread = threading.Thread
		self.frame_width = 0
		self.frame_height = 0
		self.image_data = bytearray
		self.connected = False
		self.ip = '192.168.0.241' # socket.gethostbyname(socket.gethostname())

	def client_thread(self, client_socket, address):
		self.connected = True

		stream = client_socket.recv(1024)
		if not stream:
			self.connected = False
		self.frame_width = int(stream)

		stream = client_socket.recv(1024)
		if not stream:
			self.connected = False
		self.frame_height = int(stream)

		while(self.connected):
			data = bytearray()
			length = 0
			while (length < self.frame_width*self.frame_height*4):
				stream = client_socket.recv(self.frame_width*self.frame_height*4 - length)
				data += stream
				if not stream:
					self.connected = False
					break
				length = len(data)
			if self.connected:
				self.image_data = data			
				self.img = Image.frombytes("RGB", (self.frame_width, self.frame_height), bytes(data), "raw", "BGRX")
			

		
	def start_server(self):
		self.thread = threading.Thread(target=self.run_server, daemon=True)
		self.thread.start()

	def stop_server(self):
		self.run = False
		self.thread.join()
	
	def run_server(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((self.ip, 1024))
		server_socket.listen(1) #listen to 1 client
		
		while self.run:
			( client_socket, address ) = server_socket.accept()
			ct = self.client_thread(client_socket, address)
			if(ct != None):
				ct.run()
	
