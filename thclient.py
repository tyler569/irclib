#!/usr/bin/env python3.4

"""
IRC simple threaded IRC client on top of irc.py

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

import irc
import threading

def ircRth(x):
	for line in x.read_lines():
		print(line.nick, ":", line.trail)
		
def main():
	CHANNEL = "#channel"
	NICK = "nickname"

	x = irc.client()
	x.printing = False

	x.connect("irc.freenode.net")
	x.ident("username", "hostname", "realname")
	x.nick(NICK)
	x.join(CHANNEL)
	
	t = threading.Thread(target=ircRth, args=(x,))
	t.start()
	
	while True:
		inp = input()
		x.privmsg(CHANNEL, inp)
	
if __name__ == "__main__":
	main()
	
