#irclib

IRC library for python 3.4+ using a class-based API

##Example

```python
from irclib.client.baseclient import BaseClient

class MyClient(BaseClient):
	def greeting(self, line) -> "JOIN":
		self.privmsg(self.channel, "Hello! :D")

x = MyClient(("server", port), ("user_name", "host_name", "real_name"), "nickname", "#channel")

x.run()
```
