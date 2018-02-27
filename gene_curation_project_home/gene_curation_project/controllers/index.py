#!/usr/bin/python

import os

import flask
#from flask import request, render_template
from flask import current_app, render_template, send_from_directory

#from . import valueFromRequest

index_page = flask.Blueprint("index_page", __name__)

@index_page.route("/", methods=['GET'])
def index():
	''' Index page. '''
	templateDict = {}
	
	return render_template("index.html", **templateDict)

# This will provide the favicon for the whole site. Can be overridden for
# a single page with something like this on the page:
#    <link rel="shortcut icon" href="static/images/favicon.ico">
#
@index_page.route('/favicon.ico')
def favicon():
	static_images_dir = directory=os.path.join(current_app.root_path, 'static', 'images')
	return send_from_directory(static_images_dir, filename='favicon.ico')#, mimetype='image/vnd.microsoft.icon')

@index_page.route('/robots.txt')
def robots():
	robots_path = os.path.join(current_app.root_path, 'static')
	return send_from_directory(robots_path, "robots.txt")
