#!/usr/bin/env python
#
# Wrapper for displaying grid information in real time with monitoring updates
#
# Apparently subprocess.Pipe crashes when output is over 64Kb

import os.path
import yaml
import glob
import uuid
from flask import Flask, url_for, render_template
from flask import request, session
from flask import make_response
import subprocess
import re

app = Flask(__name__)

configurationfile = 'gridpy.yaml'
config = {}

#
# init config information on startup
#
def init():
        configfile = open(configurationfile, 'r')
        global config
        config = yaml.load(configfile)
        print config
        configfile.close()

"""Execute a command with a set of options"""
def execute(command, option):
	p = subprocess.Popen([command, option], stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out, err

"""Parse the table output into HTML"""
def parse_table(o):

	olines = o.split("\n")

	out = "<table>"	

	out += "<tr>"	
	headerline = re.split("\s+", olines[0])
	for part in headerline:
		out += "<td><b>" + part + "</b>"
		out += "</td>"
	out += "</tr>"

	for line in olines[1:]:
		
		if line is not "" and not line.startswith("--"):	
			line = line.strip()			
			out += "<tr>"
			l_info = re.split("\s+", line)			
			for part in l_info:
				if part is not None and part is not "":				
					out += "<td>" + part + "</td>"
				else:					
					out += "<td>| n/a |</td>"

			out += "<td>clear</td>"
			out += "</tr>"
		
	out += "</table>"
	return out

"""Return queue info"""
def queue_info():

	out = ""	
	p = subprocess.Popen(["qstat", "-f"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = p.communicate()

	if o is not None:
		out = "<p>Queue View</p>"
		out += parse_table(o)
	else:
		print "Could not retrieve queue info output from qstat: " + e

	return out

"""Return job info"""
def jobs_info():
	
	p = subprocess.Popen(['qstat', '-u', '*'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = p.communicate()

	if o is not None:
		out = "<p style='bold'>Jobs View</p>"
		out += parse_table(o)
	else:
		print "Could not retrieve job info output from qstat: " + e

	return out

@app.route("/jobs/<gridjobid>")
def job_detail(gridjobid):
	print "received %s " % gridjobid	
	# TODO: Get job detail by id (qstat)
	return render_template("jobdetail.html")

@app.route("/users/<username>")
def job_detail(username):

	# TODO: Error handling
	#if request is None or request.form is None:
    	#return render_template('list.html',error='no search expression specified')
    #thing = request.form['expression']

	print "received %s " % username
	# TODO: Get jobs by username	

	return render_template("jobdetail.html")

"""Index"""
@app.route("/")
def index():	
    htmlout = "<b style='bold'>Grid Overview</b>"    
    htmlout += queue_info()
    htmlout += jobs_info()
    return render_template('list.html')   

if __name__ == "__main__":
	init()
	app.debug = True
	app.run(host='0.0.0.0')