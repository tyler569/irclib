
def pong(irc, line):
	"""Implements responding to server pings

	do not call or modify
	"""
	send = "PONG :{}".format(line.trail)
	irc._send(send)

