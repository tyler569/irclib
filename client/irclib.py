"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

import socket
from collections import namedtuple, defaultdict

from client.parser import IRCLine


class Client(object):
	"""Client object makes connection to IRC server and handles data

	example usage:
	x = irclib.client()
	x.connect(("irc.freenode.net", 6667))
	x.ident(("username", "hostname", "realname"))
	x.nick("nickname")
	x.join("#channel")
	"""
	#TODO : update usage example

	def __init__(self):
		"""Initialiser creates an unbound socket"""
		self.sock = socket.socket(socket.AF_INET)
		self.printing = True
		self.read_line_enable = False
		self.regd_funcs = defaultdict(list)
		

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

	def ident(self, names):
		"""Sends client identity to server,

		Can take either an arbitrary iterable eqivalent to
		[user, host, real]
		or a dict of schema:
		{'user':user, 'host':host, 'real':real}
		"""
		if isinstance(names, dict):	
			send = "USER {user} HOST {host} bla:{real}".format(**names)
		else:
			send = "USER {} HOST {} bla:{}".format(*names)
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

	def privmsg(self, target, message):
		"""Sends a message to <target>

		Can be channel or individual
		"""
		send = "PRIVMSG {} :{}".format(target, message)
		self._send(send)

	def register_func(self, cmd, func):
		"""Register a command to an IRC code or chat command
		NB: when registering a user command (from chat) ensure you use
		a prefix to avoid confising with normal chats or server commands
		"""
		self.regd_funcs[cmd].append(func)
	
	def register_dec(self, cmd):
		"""Decorator to register a command
		for example:
		x = Client()
		
		@x.register_dec("PING")
		def pong(irc, line):
			#do stuff
		"""
		def wrapper(func):
			self.register_func(cmd, func)
			return func
		return wrapper

	def get_registered(self):
		"""Return the defaultdict of registered funcs"""
		return self.regd_funcs

	def _handle_register(self, p_line):
		"""Handling of registered operations"""
		if p_line.command in self.regd_funcs:
			for func in self.regd_funcs[p_line.command]:
				func(self, p_line)
		elif p_line.usrcmd in self.regd_funcs:
			for func in self.regd_funcs[p_line.usrcmd]:
				func(self, p_line)
	

	def run(self, sock=None, recv_buffer=1024, delim="\r\n"):
		"""Run irc program"""
		#Adapted from https://synack.me/blog/using-python-tcp-sockets

		#Sets the socket to the object's socket if no name provided
		sock = sock or self.sock

		buffer = ""
		data = True
		while data:
			data = sock.recv(recv_buffer)
			buffer += data.decode('latin1')

			while buffer.find(delim) != -1:
				line, buffer = buffer.split(delim, 1)

				if self.printing:
					print(">> " + line)
				p_line = IRCLine(line).parsed
				self._handle_register(p_line)

	def alt_run(self, sock=None):
		sock = sock or self.sock

		for line in sock.makefile():
			if self.printing:
				print((">> " + line).rstrip('\r\n'))
			p_line = IRCLine(line).parsed
			self._handle_register(p_line)

