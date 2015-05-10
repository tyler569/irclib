#!/usr/bin/env python3

"""
Example Client for irclib

Copyright (C) 2014, 2015 Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from irclib.baseclient import BaseClient


class MyIRC(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmdchar = "~"

    def handle_JOIN(self, line):
        if line.nick == self.nick:
            self.privmsg("Hello everybody! Do ~help")

    def cmd_HELP(self, line):
        self.privmsg("You can do ~test or ~pm", target=line.nick)

    def cmd_TEST(self, line):
        self.privmsg("This is a test, it worked too, how about that!",
            target=line.nick)

if __name__ == "__main__":
    irc = MyIRC(
        ("server.ip", 6667),
        ("usern", "hostn", "realn"),
        "nickn",
        "#channel"
    )

    irc.run()
