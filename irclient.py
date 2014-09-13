#!/usr/bin/env python3

"""
Test Client for irclib

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

#PyYAML http://pyyaml.org/ 
#pip install pyyaml
import yaml

from client.irclib import Client

if __name__ == "__main__":
	with open("./config.yml", "r") as f:
		conf = yaml.load(f)

	x = Client()

	x.connect((conf["connection"]["server"], conf["connection"]["port"]))
	x.ident(conf["names"])
	x.nick(conf["nick"])

	@x.register_dec("MODE")
	def join(irc, line):
		irc.join(conf["channel"])

	
	@x.register_dec("PING")
	def _pong(irc, line):
		"""Implements responding to server pings

		do not call or modify
		"""
		send = "PONG :{}".format(line.trail)
		irc._send(send)

	@x.register_dec("!hello")
	def test(irc, line):
		irc.privmsg(conf["channel"], "Test successful")


	x.alt_run()
