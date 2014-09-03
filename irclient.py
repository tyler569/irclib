#!/usr/bin/env python3

"""
Test Client for irclib

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from client.irclib import Client
from private import *
#This file sets local variables such as channel and nicknames

x = Client()

x.connect(SERVER)
x.ident(USERN, HOSTN, REALN)
x.nick(NICK)

def join(irc, line):
	irc.join(CHANNEL)

def bye(irc, line):
	irc.privmsg(CHANNEL, "ohai <3")
	irc.privmsg(CHANNEL, "bai <3")

x.register("MODE", join)
x.register("JOIN", bye)

x.run()
