#!/usr/bin/python

# from flask import request #, make_response
import flask
import sqlalchemy

from flask import request, render_template

from . import valueFromRequest

from ..model import Database
from ..model.ModelClasses import Account, Gene, Flag, FlagAnnotation, Curation

gene_page = flask.Blueprint("gene_page", __name__)

db = Database()
session = db.Session()

# Note: add to __all__ in __init__.py file
@gene_page.route('/gene', methods=["GET"])
def gene():
	''' Documentation here. '''
	templateDict = {}

	gene_id = valueFromRequest(key="id", request=request)
	user_id = valueFromRequest(key="user", request=request)
	flag_label = valueFromRequest(key="flag", request=request)

	gene_query = session.query(Gene)

	# JOIN statements
	# ---------------
	if any([user_id, flag_label]):
		gene_query = gene_query.join(Curation)
		if user_id:
			gene_query = gene_query.join(Account)
		if flag_label:
			gene_query = gene_query.join(Flag)

	# FILTER statements
	if gene_id:
		gene_query = gene_query.filter(Gene.gene_id==gene_id)
	if flag_label:
		gene_query = gene_query.filter(Flag.label==flag_label)
	if user_id:
		gene_query = gene_query.filter(Account.pk==user_id)
		
	genes = gene_query.all()
	
	if len(genes)==1:
		templateDict["users"] = [x.account for x in genes[0].curations]
	
	flags = session.query(Flag).all()
	
	#print(flags)
	templateDict["flags"] = flags
	templateDict["genes"] = genes
	
	return render_template("genes.html", **templateDict)
