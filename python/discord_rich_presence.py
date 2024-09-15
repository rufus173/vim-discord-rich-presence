#!/usr/bin/python3
import socket
import json
import struct
import os
import uuid
import sys
import time
class discord_ipc:
	def __init__(self,pid,discord_socket_path="/tmp/discord-ipc-0"):
		#connect to discords ipc
		try:
			self.sock = socket.socket(socket.AF_UNIX)
			self.sock.connect(discord_socket_path)
			self.sock.settimeout(1)
			self.pid = pid
			self.start_time = int(time.time())
		except:
			return -1
	def stop(self):
		try:
			self.sock.close()
		except:
			pass

	def send(self,data,opcode = 1):
		try:
			data = json.dumps(data, separators=(",",":")).encode()
			header = struct.pack("<II",opcode,len(data))
	
			#print(f"h:{header}")
			self.sock.send(header)
			#print(f"b:{data}")
			self.sock.send(data)
		except:
			return -1

	def recv(self):
		try:
			#get response
			raw_header = self.sock.recv(8)
			op, header = struct.unpack("<II",raw_header)
			data = self.sock.recv(header).decode()
			data_json = json.loads(data)
			return data_json
		except:
			return -1

	def handshake(self):
		#prepare a handshake
		client_id = "439476230543245312" #vim bot
		#client_id = "887774122141167638" my bot
		handshake = {'v': 1, 'client_id': client_id}

		#handshake
		status = self.send(handshake,0)
		if status == -1:
			return -1
		#get hanshake response
		status = self.recv()
		if status == -1:
			return -1

	def set_presence(self,details="Editing a file",state="Type unknown"):
		#prepare activity
		activity = {
			"details":details,
			"state":state,
			"timestamps":{
				"start":self.start_time
			},
		}

		#prep new rich presence data
		data = {
			"cmd":"SET_ACTIVITY",#SET_ACTIVITY
			"args":{
				"pid": self.pid,#so discord knows when the "game" closes
				"activity":activity,
			},
			"nonce": str(uuid.uuid4()),
		}

		#send presence
		status = self.send(data)
		status = self.recv()
		if status == -1:
			return -1

if __name__ == "__main__":
	discord = discord_ipc(os.getpid())
	status = discord.handshake()
	if status == -1:
		print("could not handshake")
	while True:
		time.sleep(1)
		status = discord.set_presence()
		if status == -1:
			break
		print(status)
