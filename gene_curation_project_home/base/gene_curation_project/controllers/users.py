#!/usr/bin/python

# from flask import request #, make_response
import flask
import sqlalchemy

from flask import request, render_template

from . import valueFromRequest

from ..model import Database
from ..model.ModelClasses import Account, Gene, Flag, FlagAnnotation, Curation

user_page = flask.Blueprint("user_page", __name__)

db = Database()
session = db.Session()

# Note: add to __all__ in __init__.py file
@user_page.route('/user', methods=["GET"])
def user():
	''' Documentation here. '''
	templateDict = {}

	userId = valueFromRequest(key="id", request=request)

	try:
		users = [session.query(Account).filter(Account.pk==userId).one()]
	except sqlalchemy.orm.exc.NoResultFound:
		users = session.query(Account).all()
	
	templateDict["users"] = users
	print(type(users[0].curations[0].timestamp))
	return render_template("users.html", **templateDict)
