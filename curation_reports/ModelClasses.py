#!/usr/bin/python

import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from DatabaseConnection import DatabaseConnection

db = DatabaseConnection()
Base = db.Base

class Account(Base):
    __tablename__ = 'account'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):	
        return "<Account (pk={0}, email='{1}')>".format(self.pk, self.email)
    
    @property
    def genesCurated(self):
    	session = Session.object_session(self) 
    	return session.query(Gene).join(Curation, Account)\
    							  .filter(self.pk==Curation.account_pk)\
    							  .order_by(Gene.gene_id)\
    							  .distinct()\
    							  .all()
    	
class Flag(Base):
    __tablename__ = 'flag'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Flag (pk={0})>'.format(self.pk)

class FlagAnnotation(Base):
    __tablename__ = 'flag_annotation'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<FlagAnnotation (pk={0})>'.format(self.pk)

class Curation(Base):
    __tablename__ = 'curation'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Curation (pk={0})>'.format(self.pk)

class CurationToFlagAnnotation(Base):
    __tablename__ = 'curation_to_flag_annotation'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<CurationToFlagAnnotation (curation_pk={0}, flag_annotation_pk={1})>'.format(self.curation_pk,flag_annotation_pk)

class Gene(Base):
    __tablename__ = 'gene'
    __table_args__ = {'autoload':True, 'schema':'curation'}

    def __repr__(self):
        return '<Gene (pk={0}, id={1})>'.format(self.pk, self.gene_id)

# Relationships
# -------------
Curation.account = relationship(Account, backref="curations")
Curation.gene = relationship(Gene, backref="curations")
Curation.flag = relationship(Flag, backref="curations")
Curation.flagAnnotation = relationship(FlagAnnotation,
									   secondary=CurationToFlagAnnotation.__table__,
									   backref="curations")

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

