#!/usr/bin/python

# API endpoint for gene curation.

# from flask import request #, make_response

import json
from datetime import datetime

import flask
import sqlalchemy
from flask import request, render_template
from flask import current_app as app

#from .. import app
from . import valueFromRequest

from ..model import Database
from ..model.ModelClasses import Account, Gene, Flag, FlagAnnotation, Curation

curate_report_page = flask.Blueprint("curate_report_page", __name__)

db = Database()

# Note: add to __all__ in __init__.py file
#@app.route('/curate', methods=["POST"])
@curate_report_page.route('/curate_report', methods=["GET"])
def curate_report():
	''' Documentation here. '''
#	templateDict = {}
	
	data = request.get_json()
	
	app.logger.debug(json.dumps(data))
	
	session = db.get_session()

	accounts = session.query(Account).all()
#	app.logger.info("info statement")
	print("Accounts: {}".format(accounts))
	
	return ('', 204) # 204 NO CONTENT
	#return render_template("template.html", **templateDict)
