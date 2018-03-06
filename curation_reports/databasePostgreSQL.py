#!/usr/bin/python

''' This file handles a PostgreSQL database connection using SQLAlchemy.
	
	The example given is for a PostgreSQL database, but can be modified for any other.
'''

from flask import current_app as app

from DatabaseConnection import DatabaseConnection

try:
	db_info
except NameError:
	# only need to define this once
	db_info = dict()
	try:
		db_info["host"] = "brie"
		db_info["database"] = "postgres"
		db_info["user"] = "admin"
		db_info["password"] = ''
		db_info["port"] = 5432
	except KeyError:
		app.logger.debug("ERROR: an expected database parameter was not found.")

# This format is only usable with PostgreSQL 9.2+
dsn = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**db_info)
database_connection_string = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(**db_info)


try:
	db = DatabaseConnection() # DatabaseConnection is a singleton
except AssertionError:
	# only need to define this once
	db = DatabaseConnection(database_connection_string=database_connection_string)
	engine = db.engine
	metadata = db.metadata
	Session = db.Session
	Base = db.Base
except KeyError as e:
	print("Necessary database configuration value not defined.")
	raise e

