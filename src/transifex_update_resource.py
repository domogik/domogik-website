#!/usr/bin/python
from transifex.api import TransifexAPI

# Replace `username` and `password` here with your own username and password
t = TransifexAPI('fritz.smh@gmail.com', 'Domoi18n', 'http://transifex.com')
t.ping()
