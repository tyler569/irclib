"""
Base client class for my IRC clientside library

Copyright (C) 2014, 2015 Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from irclib.baseirc import BaseIRC


class BaseClient(BaseIRC):
    def __init__(self, *args, **kwargs):
        """Initiates connection"""
        super().__init__(*args, **kwargs)
        self.connect()
        self.ident()
        self.set_nick()
        self.join()

    def handle_PING(self, line):
        """Implements PONG"""
        send = "PONG :{}".format(line.trail)
        self._send(send)

    def handle_PRIVMSG(self, line):
        """Calls cmd_<word> when command is received"""
        try:
            if line.trail[0] != self.cmdchar:
                return
        except AttributeError:
            return
        try:
            getattr(self, "cmd_" + line.trail.split()[0][1:].upper())(line)
        except AttributeError:
            return
