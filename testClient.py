#!/usr/bin/env python3.4

"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
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
