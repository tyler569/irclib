"""
Base client class for my IRC clientside library

Copyright (C) 2014, Tyler Philbrick
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

    def handle_PING(self, line):
        """Implements PONG"""
        send = "PONG :{}".format(line.trail)
        self._send(send)

    def handle_376(self, line):
        """Sends JOIN message at the end of the MOTD"""
        self.join()
