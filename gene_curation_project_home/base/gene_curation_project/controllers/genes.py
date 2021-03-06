#!/usr/bin/python

# from flask import request #, make_response
import flask
import sqlalchemy
from sqlalchemy import func

from flask import request, render_template

from . import valueFromRequest

from ..model import Database
from ..model.ModelClasses import Account, Gene, GeneTree, GeneToGeneTree, Flag, FlagAnnotation, Curation

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
	tree_id = valueFromRequest(key="tree_id", request=request)
	set_id = valueFromRequest(key="set_id", request=request)
	min_user_count = int(valueFromRequest(key="min_users", request=request))

	gene_query = session.query(Gene)

	# JOIN statements
	# ---------------
	if any([user_id, flag_label, tree_id, set_id, min_user_count]):
		gene_query = gene_query.join(Curation)
		if (user_id or min_user_count):
			gene_query = gene_query.join(Account)
		if flag_label:
			gene_query = gene_query.join(Flag)
		if (tree_id or set_id):
			gene_query = gene_query.join(GeneToGeneTree,GeneTree)

	# FILTER statements
	if gene_id:
		gene_query = gene_query.filter(Gene.gene_id==gene_id)
	if flag_label:
		gene_query = gene_query.filter(Flag.label==flag_label)
	if user_id:
		gene_query = gene_query.filter(Account.pk==user_id)
	if tree_id:
		gene_query = gene_query.filter(GeneTree.tree_id==tree_id)
	if set_id:
		gene_query = gene_query.filter(GeneTree.set_id==set_id)

	if min_user_count:
		gene_query = gene_query.distinct(Gene.pk)
		gene_query = gene_query.group_by(Gene.pk)
		gene_query = gene_query.having(func.count(Account.pk) >= min_user_count)

		
	print("before query")
	genes = gene_query.all()
	print("after query")
	
	
	if len(genes)==1:
		templateDict["users"] = [x.account for x in genes[0].curations]

	print("before session query")
	
	flags = session.query(Flag).all()
	
	print(flags)
	templateDict["flags"] = flags
	templateDict["genes"] = genes
	
	return render_template("genes.html", **templateDict)
