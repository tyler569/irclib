#irclib

IRC library for python 3.4+ using a class-based API

##Example

```python
from irclib.baseclient import BaseClient

class MyIRC(BaseClient):
    def handle_JOIN(self, line):
        if line.nick == self.nick:
            self.privmsg("Hello everyone :D")
        else:
            self.privmsg("Hello " + line.nick)
    def handle_PART(self, line):
        self.privmsg("I miss him already D:")

bot = MyIRC(
    ("server.ip", 6667),
    ("usern", "hostn", "realn"),
    "nickn",
    "#channel"
)
    
bot.run()
```
