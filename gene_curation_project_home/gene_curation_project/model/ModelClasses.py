#!/usr/bin/python

import sqlalchemy
from sqlalchemy.orm import relationship

from .DatabaseConnection import DatabaseConnection

db = DatabaseConnection()
Base = db.Base

class Account(Base):
    __tablename__ = 'Account'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return "<Account (pk={0}, email='{1}')>".format(self.pk, self.email)

class Opinion(Base):
    __tablename__ = 'opinion'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Opinion (pk={0})>'.format(self.pk)

class Curation(Base):
    __tablename__ = 'curation'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Curation (pk={0})>'.format(self.pk)

class Gene(Base):
    __tablename__ = 'gene'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Gene (pk={0})>'.format(self.pk)

# Relationships
# -------------
Curation.account = relationship(Account, backref="curations")
Curation.gene = relationship(Gene, backref="curations")
Curation.opinion = relationship(Opinion, backref="curations")

#---------
# Test that all relationships/mappings are self-consistent.
#---------
from sqlalchemy.orm import configure_mappers
try:
	configure_mappers()
except RuntimeError as error:
	import inspect, os
	
	print ("{0}:".format(inspect.getfile(inspect.currentframe()) +
	"An error occurred when verifying the relationships between the database tables." + 
	"Most likely this is an error in the definition of the SQLALchemy relationships-" +
	"see the error message below for details."))
	
	print('Error type: {0}'.format(sys.exc_info()[0]))
	print('Error value: {0}'.format(sys.exc_info()[1]))
	print('Error trace: {0}'.format(sys.exc_info()[2]))
	sys.exit(1)

