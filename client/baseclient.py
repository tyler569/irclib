"""
Base client class for my IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from client.baseirc import BaseIRC
from client.metairc import MetaIRC


class BaseClient(BaseIRC, metaclass=MetaIRC):
	def start(self) -> "IRC_START":
		"""Initiates connection"""
		self.connect()
		self.ident()
		self.set_nick()

	def pong(self, line) -> "PING":
		"""Implements PONG"""
		send = "PONG :{}".format(line.trail)
		self._send(send)
	
	def channel_join(self, line) -> "376":
		"""Sends JOIN message at the end of the MOTD"""
		self.join()
