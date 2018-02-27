#!/usr/bin/python

# from flask import request #, make_response

from flask import request, render_template
#import simplejson # Flask will use this if imported - faster, and handles Decimal objects

from gene_curation_project import app
from . import valueFromRequest

@app.route('/')
def index():
	''' This shows how to render a template. '''
	templateDict = {"header":"A header!"}
	return render_template("index.html", **templateDict)

# a page that accepts GET requests (values on the URL)
@app.route('/page.html', methods=['GET'])
def page():
	'''
	This page accepts get requests.
	'''
	# Get the parameters.
	param1 = request.args.get("param1", None) # the 2nd term is the default value
	param2 = request.args.get("param2", None)

	return "Page"

# page that accepts both GET requests and POST form values
@app.route('/anotherPage', methods=['GET', 'POST'])
def anotherPage():
	'''
	This page accepts both GET and POST requests.
	'''
	if request.method == 'POST':
		try:
			value = request.form["param1"]
		except KeyError:
			value = None # default value if key not found.
		# ... repeat for all keys ...
	elif request.method == 'GET':
		param1 = request.args.get("param1", None)
		# ... repeat for all keys ...

@app.route('/aBetterPage', methods=['GET', 'POST'])
def aBetterPage():
	'''
	If accepting both GET and POST methods, use the local
	"valueFromRequest" method (defined in controllers.__init__.py).
	This handles both methods, and you can specify whether each
	parameter value should be made lower case, returned as a Boolean
	(e.g. for flags with no value), or parsed into a list from a
	comma-separated string.
	'''
	param1 = valueFromRequest(key="param1", request=request, lower=True)
	param2 = valueFromRequest(key="param2", request=request, list=True, default="defaultValue")

	# ...do stuff...
	return "A message of love.<br><br>param1 = {0}<br>param2 = {1}".format(param1, param2)











