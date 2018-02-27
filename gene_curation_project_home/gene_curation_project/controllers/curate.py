#!/usr/bin/python

# API endpoint for gene curation.

# from flask import request #, make_response

import flask
import sqlalchemy
from flask import request, render_template
from flask import current_app as app

#from .. import app
from . import valueFromRequest

from ..model import Database
from ..model.ModelClasses import Account, Gene, Opinion, Curation

curate_page = flask.Blueprint("curate_page", __name__)

db = Database()

# Note: add to __all__ in __init__.py file
#@app.route('/curate', methods=["POST"])
@curate_page.route('/curate', methods=["POST"])
def curate():
	''' Documentation here. '''
#	templateDict = {}
	
	data = request.get_json()
	
	session = db.get_session()

	# get account by email
	try:
		account = session.query(Account).filter(Account.email==data["email"]).one()
	except sqlalchemy.orm.exc.NoResultFound:
		# create account
		account = Account()
		account.email = data["email"]
		session.add(account)
		session.commit()
	except sqlalchemy.orm.exc.MultipleResultsFound:
		app.logger.debug("Multiple accounts with same email address found: the database is incorrectly configured.")
	
	# fetch all opinions
	opinions = dict()
	for opinion in session.query(Opinion).all():
		opinions[opinion.label] = opinion
	
	for gene_dict in data["genes"]:
		gene_id = gene_dict["geneId"]
		opinion_label = gene_dict["opinion"]
		
		# look up the gene
		try:
			gene = session.query(Gene).filter(Gene.gene_id==gene_id).one()
		except sqlalchemy.orm.exc.NoResultFound:
			gene = Gene()
			gene.gene_id = gene_id
		except sqlalchemy.orm.exc.MultipleResultsFound:
			app.logger.debug("Multiple genes with same ID found: the database is incorrectly configured.")

		# create new opinion record if we see a new one
		if opinion_label in opinions:
			opinion = opinions[opinion_label]
#		else:
#			opinion = Opinion()
#			opinion.label = opinion_label
#			session.add(opinion)
#			opinions[opinion_label] = opinion

		# create a new curation record
		#
		curation = Curation()
		curation.account = account
		curation.gene = gene
		curation.opinion = opinion
			
		session.add(curation)
	
	session.commit()	

#	accounts = session.query(Account).all()
#	app.logger.info("info statement")
#	print("Accounts: {}".format(accounts))
	
	return ('', 204) # 204 NO CONTENT
	#return render_template("template.html", **templateDict)
