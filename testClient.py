#!/usr/bin/env python3.4

"""
Docstring + License Here
"""

import irc

CHANNEL = "#channel"
NICK = "nickname"

x = irc.client()
x.printing = True

x.connect("irc.freenode.net")
x.ident("username", "hostname", "realname")
x.nick(NICK)
x.join(CHANNEL)

for line in x.read_lines():
	pass
