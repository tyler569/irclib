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

        if line[0] == ":":
            self._prefix, line = spl1n(line, " ")
            self._nick = self._prefix.split("!")[0]
        else:
            self._prefix = None
            self._nick = None
        self._command, line = spl1n(line, " ")
        self._params, trail = spl1n(line, ":")
        self._params = self._params.strip().split(" ")
        if trail:
            self._params.append(trail)

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

def spl1n(string, sep):
    """Splits string once on the first occurance of sep
    returns [head, tail] if succesful, and 
    returns (string, None) if not.

    Intended for scenarios when using unpacking with an unknown string.
    """
    r = string.split(sep, 1)
    if len(r) > 1:
        return r
    else:
       return string, None

