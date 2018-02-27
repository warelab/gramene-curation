#!/usr/bin/python

# from flask import request #, make_response

from flask import request, render_template

from .. import app
from . import valueFromRequest

# Note: add to __all__ in __init__.py file
@app.route('/path')
def func_name():
	''' Documentation here. '''
	templateDict = {}
	
	
	return render_template("template.html", **templateDict)
