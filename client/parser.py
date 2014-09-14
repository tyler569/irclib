"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from collections import namedtuple

"""Parses IRC message

Input is line from the IRC server,
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

def parse(line):
	prefix = nick = params = trail = usrcmd = None

	message = namedtuple("Message",
			"raw, prefix, nick, command, params, trail, usrcmd")

	if line[0] == ":":
		prefix_end = line.find(" ")
		prefix  = line[1:prefix_end]
		bang_loc = prefix.find("!")
		if bang_loc != -1:
			nick = prefix[:bang_loc]
		else:
			nick = prefix
	else:
		prefix_end = -1

	if " :" in line:
		trail_start = line.find(" :")
		trail = line[trail_start + 2:].rstrip("\r\n")
	else:
		trail_start = len(line)

	cmd_and_params = line[prefix_end + 1:trail_start].split(" ")
	command = cmd_and_params[0]
	if len(cmd_and_params) > 0:
		params = cmd_and_params[1:]
	if trail:
		usrcmd = trail[:trail.find(" ")]
	return message(line, prefix, nick, command, params, trail, usrcmd)


