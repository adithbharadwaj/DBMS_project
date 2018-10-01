from flask import Flask, redirect, url_for, request, render_template
from queries_test import *

app = Flask(__name__)


who_is_it = None


# login page comes first
# initial page. the page that is open when we start the server in localhost:5000
@app.route('/')
def login():
	return render_template('login.html')


# getting the details of a student from a form (in the html)
# and using those details to render a template that dynamically displays the details in a page
# the url in the login.html is of the form <form action = "http://localhost:5000/details" method = "POST">
# this url specifies where to go. for now, it points to the details page and hence, when the user clicks on submit, the details page is rendered. 
# if this url is of the form "http://localhost:5000/login", then it goes to the login page described by the login function that is given below. 
@app.route('/verify', methods = ['POST', 'GET'])
def details():

	if request.method == 'POST':
		user = request.form['usn']
		who = check_login(user)

		if(who == 'User'):
			who_is_it = 'U'
		elif(who == 'Core'):
			who_is_it = 'C'
		elif(who == 'Office'):
			who_is_it = 'O'

		else:
			who_is_it = 'N'
			return render_template('verify.html', user = 'Not a member. please register. ')

		return render_template('home.html', user = who)


@app.route('/insertmembers')
def insert_members():
	return render_template('insert_members.html')

@app.route('/events')
def disp_events():
	return render_template('events.html')


@app.route('/insertcore')
def insert_core_members():
	return render_template('insert_core.html')

@app.route('/delete')
def disp_delete_page():
	return render_template('delete.html')


@app.route('/deletemember', methods = ['POST', 'GET'])
def delete_member():

	if(request.method == 'POST'):
		usn_st = request.form['usn_delete']

		delete_st(usn_st)

		return render_template('home.html')



@app.route('/InsertMembersForm', methods = ['POST', 'GET'])
def insert_members_form():

	if(request.method == 'POST'):
		name = request.form['name']
		usn = request.form['usn']
		year = request.form['year']
		branch = request.form['branch']
		sem = request.form['semester']
		no_events = request.form['number_of_events_attended']
		no_of_comps = request.form['number_of_competitions']

		insert_student(usn, name, year, sem, branch, no_events, no_of_comps)

		return render_template('home.html')

@app.route('/InsertCoreForm', methods = ['POST', 'GET'])
def insert_core_form():

	if(request.method == 'POST'):
		name = request.form['name']
		usn = request.form['usn']
		year = request.form['year']
		branch = request.form['branch']
		sem = request.form['semester']
		pod = request.form['pod']

		insert_core(usn, name, year, sem, branch, pod)

		return render_template('home.html')




# redirects the user who logs in to the page that contains the hello() function (the /user/<name> page)
@app.route('/login', methods = ['POST', 'GET'])
def log():

	if request.method == 'POST':
		user = request.form['Name']
		return redirect(url_for('hello', name = user))
	else:
		val = request.args.get('name')
		return redirect(url_for('student_details'))


if __name__ == '__main__':
	app.debug = True # debug is used for developing since it allows us to make changes in the python file without having to restart the server again and again.
	app.run()