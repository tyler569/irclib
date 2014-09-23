#!/usr/bin/env python3

"""
Example Client for irclib

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from irclib.baseclient import BaseClient


class MyIRC(BaseClient):
    def hello_world(self, line):
        if line.nick == self.nick:
            self.privmsg("Hello everyone :D")
        else:
            self.privmsg("Hello " + line.nick)


if __name__ == "__main__":
    irc = MyIRC2(
        ("server.ip", 6667),
        ("usern", "hostn", "realn")
        "nickn",
        "#channel"
    )
        
    irc.run()
