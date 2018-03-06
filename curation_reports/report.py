#!/usr/bin/env python

import sqlalchemy

from databasePostgreSQL import db
from ModelClasses import Account

session = db.Session()

users = session.query(Account).all()
#user = users[0]

#for user in users:
#	print("{0} {1}".format(len(user.genesCurated),
#						   len(set([x.gene_id for x in user.genesCurated]))))

cshl_users = session.query(Account).filter(Account.email.like('%cshl%')).all()

for user in cshl_users:
	print("User: {0}, gene count: {1}".format(user.email, len(user.genesCurated)))