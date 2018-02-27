#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script is used to launch gene_curation_project.

Application initialization should go here.

'''
import argparse

from flask import Flask

# =====================================
# Set these values for your application
# =====================================
conf = dict()

conf["usingSQLAlchemy"] = True
conf["usingPostgreSQL"] = True

# These options only apply when the app is served in a production mode.
conf["usingSentry"]		= False	# only for use in production mode
conf["sentryDSN"]		= "insert your Sentry DSN here, e.g. 'https://...'"
conf["usingUWSGI"]		= True # only applies to serving the app in a production mode


# --------------------------
# Parse command line options
# --------------------------
parser = argparse.ArgumentParser(description='Script to start the application server.')
parser.add_argument('-d','--debug',
                    help='Launch app in debug mode.',
                    action="store_true",
                    required=False)
parser.add_argument('-p','--port',
                    help='Port to use in debug mode.',
                    default=5000,
                    type=int,
                    required=False)
parser.add_argument('-r','--rules',
                    help='List registered rules.',
                    action="store_true",
                    default=False,
                    required=False)

args = parser.parse_args()

# -------------------
# Create app instance
# -------------------
from gene_curation_project import create_app

app = create_app(debug=args.debug, conf=conf) # actually creates the Flask application instance

# -----------------------------------------
# If using SQLAlchemy, uncomment this block
# -----------------------------------------
# if conf["usingSQLAlchemy"]:
# 
# 	# Can't create the database connection unless we've created the app
# 	from gene_curation_project.model.database import db
# 	
# 	# crate 'Database' instance, connect to database
# 	#
# 	
# 	
# 	@app.teardown_appcontext
# 	def shutdown_session(exception=None):
# 	   ''' Enable Flask to automatically remove database sessions at the
# 	   	end of the request or when the application shuts down.
# 	   	Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
# 	   '''
# 	   db.Session.remove()

# ------------------------------------
# Register Flask modules (if any) here
# ------------------------------------
#app.register_module(xxx)

# Useful for debugging - specify the command line option "-r"
# to display the list of rules (valid URL paths) available.
#
# Ref: http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app
# Ref: http://stackoverflow.com/questions/17249953/list-all-available-routes-in-flask-along-with-corresponding-functions-docstrin
if args.rules:
    for rule in app.url_map.iter_rules():
        print("Rule: {0} calls {1} ({2})".format(rule, rule.endpoint, ",".join(rule.methods)))

if __name__ == "__main__":
    '''
    This is called when this script is directly run.
    uWSGI gets the "app" object (the "callable") and runs it itself.
    '''
    if args.debug:
        # If running on a remote host via a tunnel, not that
        # Safari blocks some high ports (e.g.port 6000)
        # Ref: http://support.apple.com/kb/TS4639
        #
        # By default, app is only available from localhost.
        # To make available from any host (caution!!),
        # pass "host='0.0.0.0'" as a parameter below.
        #
        app.run(debug=args.debug, port=args.port, host='0.0.0.0')
    else:
        app.run()

# PLACE NO CODE BELOW THIS LINE - it won't get called. "app.run" is the main event loop.

