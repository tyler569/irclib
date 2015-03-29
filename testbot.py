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

    def cmd_PM(self, line):
        params = line.trail.split()
        if len(params) == 2:
            self.privmsg("This is a PM for " + params[1], target=params[1])
        elif len(params) > 2:
            self.privmsg(" ".join(params[2:]), target=params[1])
        elif len(params) < 2:
            self.privmsg("ERROR: Not enough parameters", target=line.nick)

if __name__ == "__main__":
    irc = MyIRC(
        ("irc.server.net", 6667),
        ("user", "host", "real"),
        "nick",
        "#channel"
    )
        
    irc.run()
