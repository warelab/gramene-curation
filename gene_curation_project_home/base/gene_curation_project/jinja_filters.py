#!/usr/bin/python

'''
This file contains all custom Jinja2 filters.

Following the template below, new filters can be added here
and will be automatically registered.
'''

import flask
import jinja2
from jinja2 import Markup

# If the filter is to return HTML code and you don't want it autmatically
# escaped, return the value as "return Markup(value)".

blueprint = flask.Blueprint('jinja_filters', __name__)

# Ref: http://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask

# place these two decorators above every filter
@jinja2.contextfilter
@blueprint.app_template_filter()
def j2split(context, value, delimiter=None):
	if delimiter == None:
		return value.split()
	else:
		return value.split(delimiter)

@jinja2.contextfilter
@blueprint.app_template_filter()
def j2join(context, value, delimiter=","):
    return delimiter.join(value)

@jinja2.contextfilter
@blueprint.app_template_filter()
def str2datetime(context, value):
    '''
    Format date : "2017-10-28T02:20:32" -> "28 October 2017"
    '''
    #
    # This is useful: http://strftime.org
    #
    if isinstance(value, str):
        if "T" in value:
            dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            return dt # type: datetime.datetime
            #.strftime('%Y-%m-%d')