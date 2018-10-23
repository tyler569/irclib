#!/usr/bin/env python3

"""
Example Client for irclib

Copyright (C) 2014, 2015 Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

from irclib.baseirc import IRCClient


bot = IRCClient(
    ("irc.openredstone.org", 6667),
    "tbot", "Back to Python bby", "tbot",
    "#openredstone"
)


@bot.register("001")
def server_auth(bot, line):
    bot.privmsg("NickServ", "identify orepassword")
    bot.join(bot.channel)


@bot.register("JOIN")
def join(bot, line):
    print("I joined a place!")


@bot.register("PRIVMSG")
def handle_chat(bot, line):
    print("We are handling #confirmed")
    if line.nick == "tyler" and line.trail[0] == '~':
        bot.privmsg(bot.channel, "Hi!")


print(bot.callbacks)
bot.run()
