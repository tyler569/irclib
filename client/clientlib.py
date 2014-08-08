"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

import socket
from collections import namedtuple

import parser


class client(object):
	"""Client object makes connection to IRC server and handles data

	example usage:
	x = irc.client()
	x.connect(("irc.freenode.net", 6667))
	x.ident("username", "hostname", "realname")
	x.nick("nickname")
	x.join("#channel")
	for i in x.readlines():
		do things
	"""
	def __init__(self):
		"""Initialiser creates an unbound socket"""
		self.sock = socket.socket()
		self.printing = True
		
	def _send(self, message):
		"""Private method invoked by others to send on socket

		Adds \r\n at the end of messages
		"""
		if self.printing:
			print("<< " + message)
		self.sock.sendall((message + "\r\n").encode())

	def connect(self, server_info):
		"""Implements socket connection to IRC server
		
		server_info is tuple of (hostname, port)
		"""
		self.sock.connect(server_info)

	def ident(self, usern, hostn, realn):
		"""Sends client identity to server"""
		send = "USER {} HOST {} bla:{}".format(usern, hostn, realn)
		self._send(send)
	
	def nick(self, new_nick):
		"""Binds or changes client nickname

		Note that some servers require you to privmsg a nickname bot
		to verify registerd nicknames
		"""
		send = "NICK {}".format(new_nick)
		self._send(send)

	def join(self, new_channel):
		"""Implements client joining a channel"""
		send = "JOIN {}".format(new_channel)
		self._send(send)
		#TODO - 
		#Have the server's "JOIN" responce set the object's
		#current channels for retrieval
		
	def privmsg(self, target, message):
		"""Sends a message to <target>

		Can be channel or individual
		"""
		send = "PRIVMSG {} :{}".format(target, message)
		self._send(send)
	
	def _pong(self, arg):
		"""Implements responding to server pings

		do not call or modify
		"""
		send = "PONG :{}".format(arg)
		self._send(send)

	def read_lines(self, sock = None, recv_buffer = 1024, delim = "\r\n"):
		"""Generator that produces parsed lines as they come in"""
		#Adapted from https://synack.me/blog/using-python-tcp-sockets
		
		#Sets the socket to the class socket if no name provided
		#Can not be done in def due to scope of "self"
		sock = sock or self.sock
		
		buffer = ""
		data = True
		while data:
			data = sock.recv(recv_buffer)
			buffer += data.decode('latin1')
			#TODO - 
			#recall that servers can have different encodings

			while buffer.find(delim) != -1:
				line, buffer = buffer.split(delim, 1)
				
				if self.printing:
					print(">> " + line)
				p_line = parser.parse(line)
				
				if not self._preproc_line(p_line):	
					yield p_line

	def _preproc_line(self, p_line):
		"""Line preprocessor,

		deals with such details as responding to server pings
		"""
		if p_line.command == "PING":
			self._pong(p_line.trail)
			return True
		elif is_retcode(p_line.command):
			self._handle_retcode(p_line)
			return False
		return False

	def _handle_retcode(self, p_line):
		"""Handling of return codes

		This may not be implemented
		"""
		#IN HERE:
		#SOME retcodes change state info (I.E. motd stored for retrieval)
		#MOST DO NOTHING HERE
		#BUT they call an overwritable func
		pass

def is_retcode(command):
	"""Determines if the command is a return code of form \d{3}"""
	if len(command) == 3:
		try:
			int(command)
			return True
		except ValueError:
			return False
