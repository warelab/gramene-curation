#!/usr/bin/python

from __future__ import print_function
from __future__ import division

import os

'''
This is a collection of functions to customize the setup of the application,
but put here so as not to clutter up the __init__.py file.
'''

def setupJSONandDecimal():
    # -----------------------------------------------------------------------------
    # The JSON module is unable to serialize Decimal objects, which is a problem
    # as psycopg2 returns Decimal objects for numbers. This block of code overrides
    # how psycopg2 parses decimal data types coming from the database, using
    # the "float" data type instead of Decimal. This must be done separately for
    # array data types.
    #
    # See link for other data types: http://initd.org/psycopg/docs/extensions.html
    # -----------------------------------------------------------------------------
    import psycopg2
    DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        'DEC2FLOAT',
        lambda value, curs: float(value) if value is not None else None)
    psycopg2.extensions.register_type(DEC2FLOAT)

    # the decimal array is returned as a string in the form:
    # "{1,2,3,4}"
    DECARRAY2FLOATARRAY = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMALARRAY.values,
        'DECARRAY2FLOATARRAY',
        lambda value, curs: [float(x) if x else None for x in value[1:-1].split(",")] if value else None)
    #    lambda value, curs: sys.stdout.write(value))
    psycopg2.extensions.register_type(DECARRAY2FLOATARRAY)
    # -----------------------------------------------------------------------------

def setupSentry(app=None, dsn=None):
	'''
	Set up getsentry.com logging - only use when in production
	'''
	if dsn == None:
		raise Exception("A DSN must be provided to use Sentry.")
		
	from raven.contrib.flask import Sentry
	
	#dsn = <your DSN here>
	app.config['SENTRY_DSN'] = dsn
	sentry = Sentry(app)

	# --------------------------------------
	# Configuration when running under uWSGI
	# --------------------------------------
	try:
		import uwsgi
		app.use_x_sendfile = True
		# can add other uWSGI options here
	except ImportError:
		# not running under uWSGI (and presumably, nginx)
		pass

def getConfigFile(configFile=None):
	'''
	Returns the path of the named local configuration file.
	'''
	conf_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration_files', configFile)
	if os.path.isfile(conf_filepath):
		return conf_filepath
	else:
		raise Exception("Configuration file '{0}' not found.".format(conf_filepath))

