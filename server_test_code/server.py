import socket
from PIL import Image
import threading
import time
import netifaces as ni

class server():
	def __init__(self):
		self.run = True
		self.img = None
		self.thread = threading.Thread
		self.frame_width = 0
		self.frame_height = 0
		self.connected = False
		ni.ifaddresses('wlp4s0')
		self.ip = ni.ifaddresses('wlp4s0')[ni.AF_INET][0]['addr']
		# self.ip = '192.168.0.241' # socket.gethostbyname(socket.gethostname())

	def client_thread(self, client_socket, address):
		self.connected = True

		stream = client_socket.recv(4)
		if not stream:
			self.connected = False
		self.frame_width = int(stream)

		stream = client_socket.recv(4)
		if not stream:
			self.connected = False
		self.frame_height = int(stream)

		while(self.connected):
			data = bytearray()
			length = 0
			t0= time.time()
			while (length < self.frame_width*self.frame_height*3):
				stream = client_socket.recv(self.frame_width*self.frame_height*3 - length)
				data += stream
				if not stream:
					self.connected = False
					break
				length = len(data)
			if self.connected:
				self.img = Image.frombytes("RGB", (self.frame_width, self.frame_height), bytes(data), "raw", "RGB")
			t1 = time.time() - t0
			print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

			

		
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
	
