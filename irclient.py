#!/usr/bin/env python3

"""
Test Client for irclib

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

#PyYAML http://pyyaml.org/ 
#pip install pyyaml
import yaml

#from client.baseclient import BaseClient
from myirc import MyIRC2

if __name__ == "__main__":
	with open("./config.yml", "r") as f:
		conf = yaml.load(f)

	x = MyIRC2(
		(conf["connection"]["server"], conf["connection"]["port"]),
		conf["names"],
		conf["nick"],
		conf["channel"]
	)
		
	x.run()
