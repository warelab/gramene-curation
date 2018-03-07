#!/usr/bin/python

import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from .DatabaseConnection import DatabaseConnection

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
								  .all()

	def genesCuratedWithFlag(self,flag=None):
		session = Session.object_session(self) 
		return session.query(Gene).join(Curation, Account, Flag)\
								  .filter(self.pk==Curation.account_pk)\
								  .filter(Flag.label==flag)\
								  .order_by(Gene.gene_id)\
								  .all()

	def curationForGene(self,gene_id=None):
		session = Session.object_session(self)
		return session.query(Curation).join(Gene, Account)\
									  .filter(Account.pk==self.pk)\
									  .filter(Gene.gene_id==gene_id)\
									  .one()
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

	def curationsWithFlag(self,flag=None):
		session = Session.object_session(self) 
		return session.query(Curation).join(Gene, Flag)\
								  .filter(self.pk==Curation.gene_pk)\
								  .filter(Flag.label==flag)\
								  .all()

class GeneTree(Base):
	__tablename__ = 'gene_tree'
	__table_args__ = {'autoload':True, 'schema':'curation'}

	def __repr__(self):
		return '<GeneTree (pk={0}, id={1})>'.format(self.pk, self.tree_id)

class GeneToGeneTree(Base):
	__tablename__ = 'gene_to_gene_tree'
	__table_args__ = {'autoload':True, 'schema':'curation'}

	def __repr__(self):
		return '<GeneToGeneTree (gene_pk={0}, tree_pk={1})>'.format(self.gene_pk, self.tree_pk)


# Relationships
# -------------
Curation.account = relationship(Account, backref="curations")
Curation.gene = relationship(Gene, backref="curations")
Curation.flag = relationship(Flag, backref="curations")
Curation.flagAnnotation = relationship(FlagAnnotation,
									   secondary=CurationToFlagAnnotation.__table__,
									   backref="curations")
Gene.trees = relationship(GeneTree,
						  secondary=GeneToGeneTree.__table__,
						  backref="genes")

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

