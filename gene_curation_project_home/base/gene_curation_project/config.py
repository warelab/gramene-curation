#!/usr/bin/python

from __future__ import print_function, division, absolute_import, unicode_literals

'''
This class manages the runtime configuration of the application,
e.g. server information, debug mode, etc. Anything that might be
set as a constant that might vary from one running process or
server to another.

The configuration is read from ../app.config. Convenience
methods should be defined here that map to values in the configuration
file that are easy to read. One should not need to know the exact
format of the config file when accessing values (i.e. this class
abstracts the information).

'''

import json
try:
	import configparser					# renamed in Python 3 to this
except ImportError:
	import ConfigParser as configparser	# Python 2 compatibility

from .designpatterns import singleton, memoize

@singleton
class AppConfig(object):
	''' An object that contains the runtime configuration for this application. '''
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("api.config")
		self.dr2instr = None

	@memoize
	@property
	def debugMode(self):
		return self.config.getboolean("app", "debugMode")

	def databaseConnectionInfo(self):
		db_info = {}
		for key in self.config.options("db_example"):
			db_info[key] = self.config.get("db_example", key)
		return db_info