"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

"""Parses IRC message

Input is line from the IRC server,
Output is named tuple with keys:
    raw: the raw line input
    prefix: the IRC prefix including nick, user/hostname, etc
    nick: the sender's nickname (if any)
    command: the IRC command <- this is the only required part
    params: the command's parameters as a list
    trail: the IRC line's trailing section.  If the line is a
        user chat, the message is here
Any part of the line not included is None
"""

class Line(object):
    def __init__(self, line):
        self._raw = line
        self._prefix = None
        self._nick = None
        self._command = None
        self._params = None
        self._trail = None

        if line[0] == ":":
            prefix_end = line.find(" ")
            self._prefix = line[1:prefix_end]
            bang_loc = self._prefix.find("!")
            if bang_loc != -1:
                self._nick = self._prefix[:bang_loc]
            else:
                self._nick = self._prefix
        else:
            prefix_end = -1

        if " :" in line:
            trail_start = line.find(" :")
            self._trail = line[trail_start + 2:].rstrip("\r\n")
        else:
            trail_start = len(line)

        cmd_and_params = line[prefix_end + 1:trail_start].split(" ")
        self._command = cmd_and_params[0]
        if len(cmd_and_params) > 0:
            self._params = cmd_and_params[1:]

    @property
    def raw(self):
        return self._raw

    @property
    def prefix(self):
        return self._prefix

    @property
    def nick(self):
        return self._nick

    @property
    def command(self):
        return self._command

    @property
    def params(self):
        return self._params

    @property
    def trail(self):
        return self._trail

