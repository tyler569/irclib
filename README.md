
# Extensible Event-based IRC Library

*Project Name* is an IRC library written in python designed to make writing bots a breeze.  *Project Name* abstracts over all of the complicated details associated with connecting to an IRC server and keeping that connection alive and allows you to describe only the functionality you want to implement.

This library is event-based, where any message from the IRC server can be an event.  These events are defined by what command the IRC server sends.  For example, if there is function defined in the bot code called "handle_KICK," the library will run it every time the IRC server sends a message where the command is "KICK."

For user commands, there is a convenience built in whereby if the first character of a private message is a "command character" defined by the bot writer, the library will run event handlers named "cmd_COMMAND."  The purpose of this is to help the bot author avoid a monolithic "hamdle_PRIVMSG" function with a massive 'if/elif' chain for possible commands.

## Short Example

A more comprehensive example is provided in 'testbot.py' above, the following is intended as a demonstrative tool to show how easy writing bots with *Project Name* can be.

```python

import irclib.BaseClient

class MyBot(irclib.BaseClient):
	def handle_JOIN(self, line):
		if line.nick == self.nick:
			self.privmsg("Hello Everyone!")

bot = MyBot(
	"server.ip",
	("username", "hostname", "realname"),
	"nickname",
	"#channel"
)

bot.run()

```

It's that simple, *Project Name* provides an expressive interface to the IRC protocol and lets you write only your application logic code, we take care of all the boilerplate for you.

