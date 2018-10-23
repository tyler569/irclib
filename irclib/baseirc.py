
# IRC clientside library
#
# Copyright (C) 2014, 2017, Tyler Philbrick
# All Rights Reserved
# For license information, see COPYING

import socket

import irclib.parser as parser


def pong(bot, line):
    bot.pong(line.trail)


class IRCClient:
    def __init__(self, server, user, real, nick, channel, printing=True):
        self.sock = socket.socket()
        self.nickname = nick
        self.channel = channel
        self.printing = printing
        self.callbacks = {"PING": pong}

        self.connect(server)
        self.ident(user, real)
        self.nick(nick)

    def raw_send(self, message):
        if self.printing:
            print("<< " + message)
        self.sock.sendall((message + "\r\n").encode())

    def connect(self, server):
        self.sock.connect(server)

    def ident(self, user, real):
        self.raw_send("USER {} 0 * :{}".format(user, real))

    def nick(self, nick):
        self.raw_send("NICK {}".format(nick))

    def join(self, channel):
        self.raw_send("JOIN {}".format(channel))

    def pong(self, message):
        self.raw_send("PONG :{}".format(message))

    def privmsg(self, message, target):
        self.raw_send("PRIVMSG {} :{}".format(target, message))

    def register(self, name):
        def reg(fn):
            self.callbacks[name] = fn
            return fn
        return reg

    def _handle_register(self, line):
        if line.command in self.callbacks:
            self.callbacks[line.command](self, line)

    def run(self):
        sockf = self.sock.makefile()

        for line in sockf:
            line = line.rstrip("\r\n")
            if self.printing:
                print((">> " + line))
            p_line = parser.Line(line)
            # print(p_line.prefix, p_line.command, p_line.params)
            print("'", p_line.command, "'")
            self._handle_register(p_line)

