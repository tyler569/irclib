"""
IRC clientside library

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

import socket
from collections import namedtuple, defaultdict

from irclib.parser import parse


class BaseIRC(object):
    """Client object makes connection to IRC server and handles data

    example usage:
    """
    #TODO : update usage example

    regd_funcs = {}

    def __init__(self, server, names, nick, channel, sock=None, printing=True):
        """Initialiser creates an unbound socket"""
        self.sock = sock or socket.socket()
        self.server = server
        self.names = names
        self.nick = nick
        self.channel = channel
        self.printing = printing

        self.__class__.regd_funcs["IRC_START"](self)

    def _send(self, message):
        """Private method invoked by others to send on socket

        Adds \r\n at the end of messages
        """
        if self.printing:
            print("<< " + message)
        self.sock.sendall((message + "\r\n").encode())

    def connect(self, server=None):
        """Implements socket connection to IRC server

        server_info is tuple of (hostname, port)
        """
        server = server or self.server
        self.sock.connect(server)

    def ident(self, names=None):
        """Sends irclib identity to server,

        Can take either an arbitrary iterable eqivalent to
        [user, host, real]
        or a dict of schema:
        {'user':user, 'host':host, 'real':real}
        """
        names = names or self.names
        if isinstance(names, dict):
            send = "USER {user} HOST {host} bla:{real}".format(**names)
        else:
            send = "USER {} HOST {} bla:{}".format(*names)
        self._send(send)

    def set_nick(self, nick=None):
        """Binds or changes irclib nickname

        Note that some servers require you to privmsg a nickname bot
        to verify registerd nicknames
        """
        nick = nick or self.nick
        send = "NICK {}".format(nick)
        self._send(send)

    def join(self, channel=None):
        """Implements irclib joining a channel"""
        channel = channel or self.channel
        send = "JOIN {}".format(channel)
        self._send(send)

    def privmsg(self, message, target=None):
        """Sends a message to <target>

        Can be channel or individual
        """
        target = target or self.channel

        send = "PRIVMSG {} :{}".format(target, message)
        self._send(send)

    def _handle_register(self, p_line):
        """Handling of registered operations"""
        if p_line.command in self.__class__.regd_funcs:
            if p_line.command in self.__class__.regd_funcs:
                self.__class__.regd_funcs[p_line.command](self, p_line)
        elif (p_line.command == "PRIVMSG" and
             p_line.usrcmd in self.__class__.regd_funcs):
            if p_line.usrcmd in self.__class__.regd_funcs:
                self.__class__.regd_funcs[p_line.usrcmd](self, p_line)
        if "ALL" in self.__class__.regd_funcs:
            self.__class__.regd_funcs["ALL"](self, p_line)

    def run(self):
        """Run IRC program"""
        sockf = self.sock.makefile()

        for line in sockf:
            if self.printing:
                print((">> " + line).rstrip('\r\n'))
            p_line = parse(line)
            self._handle_register(p_line)
