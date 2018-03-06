#!/usr/bin/python

# from flask import request #, make_response
import flask
import sqlalchemy

from flask import request, render_template

from .. import app
from . import valueFromRequest

# from ..model import Database
# from ..model.ModelClasses import Account, Gene, Flag, FlagAnnotation, Curation

template_page = flask.Blueprint("template_page", __name__)

# db = Database()

# Note: add to __all__ in __init__.py file
@template_page.route('/template') #, methods=["GET","POST"])
def template():
	''' Documentation here. '''
	templateDict = {}
	
	
	return render_template("template.html", **templateDict)
