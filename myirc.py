from client.baseclient import BaseClient

class MyIRC(BaseClient):
	def hello(self, line) -> "!hello":
		self.privmsg(self.channel, "Hello World")

class MyIRC2(MyIRC):
	def bye(self, line) -> "PART":
		self.privmsg(self.channel, "Byee :(")
