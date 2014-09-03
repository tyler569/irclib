"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from collections import namedtuple

class IRCLine(object):
	"""Parses IRC message

	Input is line from the IRC server stripped of \r\n,
	Output is named tuple with keys:
		raw: the raw line input
		prefix: the IRC prefix including nick, user/hostname, etc
		nick: the sender's nickname (if any)
		command: the IRC command <- this is the only required part
		params: the command's parameters as a list
		trail: the IRC line's trailing section.  If the line is a
			user chat, the message is here
	Any part of the line not included is None
	"""

	def __init__(self, line):
		self.line = line
		self.parsed = self.parse()


	def parse(self):
		prefix = nick = params = trail = None

		message = namedtuple("Message",
				"raw, prefix, nick, command, params, trail")

		if self.line[0] == ":":
			prefix_end = self.line.find(" ")
			prefix  = self.line[1:prefix_end]
			bang_loc = prefix.find("!")
			if bang_loc != -1:
				nick = prefix[:bang_loc]
			else:
				nick = prefix
		else:
			prefix_end = -1

		if " :" in self.line:
			trail_start = self.line.find(" :")
			trail = self.line[trail_start + 2:]
		else:
			trail_start = len(self.line)

		cmd_and_params = self.line[prefix_end + 1:trail_start].split(" ")
		command = cmd_and_params[0]
		if len(cmd_and_params) > 0:
			params = cmd_and_params[1:]
		return message(self.line, prefix, nick, command, params, trail)


