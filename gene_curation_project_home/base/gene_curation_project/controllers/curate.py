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

curate_page = flask.Blueprint("curate_page", __name__)

db = Database()

# Note: add to __all__ in __init__.py file
#@app.route('/curate', methods=["POST"])
@curate_page.route('/curate', methods=["POST"])
def curate():
	''' Documentation here. '''
#	templateDict = {}
	
	data = request.get_json()
	
	app.logger.debug(json.dumps(data))
	
	session = db.get_session()

	# get account by email
	try:
		account = session.query(Account).filter(Account.email==data["email"]).one()
	except sqlalchemy.orm.exc.NoResultFound:
		# create account
		account = Account()
		account.email = data["email"]
		session.add(account)
		#session.commit()
	except sqlalchemy.orm.exc.MultipleResultsFound:
		app.logger.debug("Multiple accounts with same email address found: the database is incorrectly configured.")
	
	# fetch all flags
	flags = dict()
	for flag in session.query(Flag).all():
		flags[flag.label] = flag

	# fetch all flag annotations
	flag_annotations = dict()
	for fa in session.query(FlagAnnotation).all():
		flag_annotations[fa.label] = fa
	
	# use a common timestamp for all entries of this curation
	timestamp = datetime.utcnow()
	
	for gene_dict in data["genes"]:
		gene_id = gene_dict["geneId"]
		flag_label = gene_dict["opinion"]
		flag_annotation_label = gene_dict.get("reason", None)
			
		# look up the gene
		try:
			gene = session.query(Gene).filter(Gene.gene_id==gene_id).one()
		except sqlalchemy.orm.exc.NoResultFound:
			gene = Gene()
			gene.gene_id = gene_id
			session.add(gene)
		except sqlalchemy.orm.exc.MultipleResultsFound:
			app.logger.debug("Multiple genes with same ID found: the database is incorrectly configured.")

		# create new flag record if we see a new one
		if flag_label in flags:
			flag = flags[flag_label]
		else:
			flag = Flag()
			flag.label = flag_label
			session.add(flag)
			flags[flag_label] = flag

		if flag_annotation_label in flag_annotations:
			flag_annotation = flag_annotations[flag_annotation_label]
		elif flag_annotation_label is None:
			flag_annotation = None
		else:
			# create new flag annotation
			flag_annotation = FlagAnnotation()
			flag_annotation.label = flag_annotation_label
			session.add(flag_annotation)
			flag_annotations[flag_annotation_label] = flag_annotation
		
		# create a new curation record
		#
		curation = Curation()
		curation.account = account
		curation.gene = gene
		curation.flag = flag
		curation.timestamp = timestamp
		if flag_annotation:
			curation.flagAnnotation.append(flag_annotation)
			
		session.add(curation)
	
	session.commit()	

#	accounts = session.query(Account).all()
#	app.logger.info("info statement")
#	print("Accounts: {}".format(accounts))
	
	return ('', 204) # 204 NO CONTENT
	#return render_template("template.html", **templateDict)
