#!/usr/bin/env python3

"""
Test Client for irclib

Copyright (C) 2014, Tyler Philbrick
All Rights Reserved
For license information, see COPYING
"""

import lib.irclib as irclib
from private import *
#This file sets local variables such as channel and nicknames

x = irclib.client()

x.connect(SERVER)
x.ident(USERN, HOSTN, REALN)
x.nick(NICK)
x.join(CHANNEL)

for i in x.read_lines(): pass
