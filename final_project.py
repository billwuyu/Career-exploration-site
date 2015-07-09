from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Career, Base, Project

import urllib2
import json
import os

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///exduu.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

#connect to database!!
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def homePage():
	output = "This is the landing page!"
	return output

@app.route('/careers/')
def allCareers():
	careers = session.query(Career).all()
	return render_template('careers.html', careers = careers)

@app.route('/careers/new', methods = ['GET', 'POST'])
def newCareer():
	if request.method == 'POST':
		newCareer = Career(name = request.form['name'], description = request.form['description'])
		session.add(newCareer)
		session.commit()
		flash("New career created!")
		return redirect(url_for('allCareers'))

	else: # handle GET request
		return render_template('newcareer.html')

@app.route('/careers/<int:career_id>/edit', methods = ['GET', 'POST'])
def editCareer(career_id):
	career = session.query(Career).filter_by(id = career_id).one()
	if career is None:
		print "career is None"
		return "No such career!"
	if request.method == 'POST':
		if request.form['name']:
			career.name = request.form['name']
		if request.form['description']:
			career.description = request.form['description']
		session.add(career)
		session.commit()
		flash("Career successfully edited")
		return redirect(url_for('allCareers'))
	else:
		return render_template('editcareer.html', career = career)

@app.route('/careers/<int:career_id>/delete', methods =  ['GET', 'POST'])
def deleteCareer(career_id):
	career = session.query(Career).filter_by(id = career_id).one()
	if career is None:
		return "No such career!"

	if request.method == 'POST':
		session.delete(career)
		session.commit()
		flash("Career deleted!")
		return redirect (url_for('allCareers'))
	else:
		return render_template('deletecareer.html', career = career)

@app.route('/careers/<int:career_id>/projects/')
def allProjects(career_id):
	career = session.query(Career).filter_by(id = career_id).one()
	projects = session.query(Project).filter_by(career_id = career_id).all()
	return render_template('projects.html', career = career, projects = projects)

@app.route('/careers/<int:career_id>/projects/new/', methods = ['GET', 'POST'])
def newProject(career_id):

	career = session.query(Career).filter_by(id = career_id).one()

	if request.method == 'POST':
		if request.form['title']:
			newProject = Project(title = request.form['title'], description = request.form['description'], career_id = career_id)
			session.add(newProject)
			session.commit()
			flash("New project created!")
			return redirect(url_for('allProjects', career_id = career_id))
		else: 
			flash("Title field must not be empty!")
			return render_template('newproject.html', career = career)

	else: # handle GET request
		return render_template('newproject.html', career = career)

@app.route('/careers/<int:career_id>/projects/<int:project_id>/')
def showProject(career_id, project_id):
	project = session.query(Project).filter_by(id = project_id).one()
	return render_template('showoneproject.html', career_id = career_id, project = project)


@app.route('/careers/<int:career_id>/projects/<int:project_id>/edit/', methods = ['GET', 'POST'])
def editProject(career_id, project_id):
	project = session.query(Project).filter_by(id = project_id).one()
	if project is None:
		return "No such project!"
	if request.method == 'POST':
		if request.form['title']:
			project.title = request.form['title']
		if request.form['description']:
			project.description = request.form['description']
		session.add(project)
		session.commit()
		flash("Project successfully edited")
		return redirect(url_for('allProjects', career_id = career_id))
	else:
		return render_template('editproject.html', project = project, career_id = career_id)

@app.route('/careers/<int:career_id>/projects/<int:project_id>/delete/', methods = ['GET', 'POST'])
def deleteProject(career_id, project_id):
	project = session.query(Project).filter_by(id = project_id).one()	
	if project is None:
		return "No such career!"

	if request.method == 'POST':
		session.delete(project)
		session.commit()
		flash("Project deleted!")
		return redirect (url_for('allProjects', career_id = career_id))
	else:
		return render_template('deleteproject.html', project = project, career_id = career_id)

@app.route('/events/')
def upcomingEvents():
	url = 'https://api.meetup.com/2/open_events?&key=6b2fb756a675b223d3c457822ce4b&country=CA&city=Toronto&time=,1w&page=10'
	data = json.load(urllib2.urlopen(url))
	events = data['results']
	output = ''

	for i in events:
		output += "<h1>%s</h1>" %i['name']
		output += "%s<br>" % i['description']

	return output
	#return render_template('events.html', events = events)



if __name__ == "__main__":
	app.secret_key = 'super_secret_key'
	app.debug = True
	#app.run(host = '0.0.0.0', port = 5000)
