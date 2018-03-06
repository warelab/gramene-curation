#!/usr/bin/python
#

import os
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool

def clearSearchPathCallback(dbapi_con, connection_record):
    '''
    When creating relationships across schemas, SQLAlchemy
    has problems when you explicitly declare the schema in
    ModelClasses and it is found in search_path.
    
    The solution is to set the search_path to "$user" for
    the life of any connection to the database. Since there
    is no schema with the same name as the user, (or shouldn't
    be here!), this effectively makes it blank.
    
    This callback function is called for every database connection.
    
    For the full details of this issue, see:
    http://groups.google.com/group/sqlalchemy/browse_thread/thread/88b5cc5c12246220
    
    dbapi_con - type: psycopg2._psycopg.connection
    connection_record - type: sqlalchemy.pool._ConnectionRecord
    '''
    cursor = dbapi_con.cursor()
    cursor.execute('SET search_path TO "$user",functions')
    dbapi_con.commit()

listen(Pool, 'connect', clearSearchPathCallback)

class DatabaseConnection(object):
	'''This class defines an object that makes a connection to a database.
	   The "DatabaseConnection" object takes as its parameter the SQLAlchemy
	   database connection string.

	   This class is best called from another class that contains the
	   actual connection information (so that it can be reused for different
	   connections).
	   
	   This class implements the singleton design pattern. The first time the
	   object is created, it *requires* a valid database connection string.
	   Every time it is called via:
	   
	   db = DatabaseConnection()
	   
	   the same object is returned and contains the connection information.
	'''
	_singletons = dict()
	
	def __new__(cls, database_connection_string=None):
		"""This overrides the object's usual creation mechanism."""

		if not cls in cls._singletons:
			assert database_connection_string is not None, "A database connection string must be specified!"
			cls._singletons[cls] = object.__new__(cls)
			
			# ------------------------------------------------
			# This is the custom initialization
			# ------------------------------------------------
			me = cls._singletons[cls] # just for convenience (think "self")
			
			me.database_connection_string = database_connection_string
			
			# change 'echo' to print each SQL query (for debugging/optimizing/the curious)
			me.engine = create_engine(me.database_connection_string, echo=False)	

			me.metadata = MetaData()
			me.metadata.bind = me.engine
			me.Base = declarative_base(bind=me.engine)
			me.Session = scoped_session(sessionmaker(bind=me.engine, autocommit=True))
			# ------------------------------------------------
		
		return cls._singletons[cls]


'''
Reference: http://www.sqlalchemy.org/docs/05/reference/orm/sessions.html#sqlalchemy.orm.sessionmaker

autocommit = True : this prevents postgres from deadlocking on long-lived session processes (e.g. a background daemon), that produces 'idle in transaction' processes in PostgreSQL.

Sample code to account for different cases (if things change for whatever reason):

if session.autocommit:
	session.begin()
<do stuff>
session.commit()

Try to minimise the work done in between session.begin() and session.commit().
'''
