#!/usr/bin/python3
import socket
import json
import struct
import os
import uuid
class discord_ipc:
	def __init__(self,discord_socket_path="/tmp/discord-ipc-0"):	
		#connect to discords ipc
		self.sock = socket.socket(socket.AF_UNIX)
		self.sock.connect(discord_socket_path)
	
	def stop(self):
		self.sock.close()

	def send(self,data,opcode = 1):
		data = json.dumps(data, separators=(",",":")).encode()
		header = struct.pack("<II",opcode,len(data))

		print(f"h:{header}")
		self.sock.send(header)
		print(f"b:{data}")
		self.sock.send(data)

	def recv(self):
		#get response
		raw_header = self.sock.recv(8)
		op, header = struct.unpack("<II",raw_header)
		data = self.sock.recv(header).decode()
		data_json = json.loads(data)
		return data_json	

if __name__ == "__main__":
	import sys
	import time
	pid = int(sys.argv[1])
	discord = discord_ipc()
	#prepare a handshake
	client_id = "439476230543245312" #vim bot
	#client_id = "887774122141167638" my bot
	handshake = {'v': 1, 'client_id': client_id}

	#handshake
	discord.send(handshake,0)
	#get hanshake response
	print(discord.recv())


	#prepare activity
	activity = {
		"details":"me when",
		"state":str(pid),
		#"assets":{
		#	"small_text":"me when small text"
		#},
	}

	#prep new rich presence data
	data = {
		"cmd":"UPDATE_ACTIVITY",#SET_ACTIVITY
		"args":{
			"pid": pid,#so discord knows when the "game" closes
			"activity":activity,
		},
		"nonce": str(uuid.uuid4()),
	}

	#send presence
	discord.send(data)
	print(discord.recv())
	discord.stop()
