from flask import Flask, redirect, url_for, request, render_template
from queries_test import *
import matplotlib.pyplot as plt

app = Flask(__name__)

# global variable to keep track of which group the user belongs to. Student, Core or office bearer.
# this helps us take care of the permissions later.
who_is_it = None

'''
---------------------------------------------------------------------------------------------
routing to Display the Pages
'''

# login page comes first
# initial page. the page that is open when we start the server in localhost:5000
@app.route('/')
def login():
	return render_template('login.html')

@app.route('/home')
def disp_home_page():
	return render_template('home.html')

@app.route('/insertmembers')
def insert_members():
	return render_template('insert_members.html')

@app.route('/events')
def disp_events():
	data = select_all_events()
	return render_template('events.html', result = data)

@app.route('/insertcore')
def insert_core_members():
	return render_template('insert_core.html')

@app.route('/delete')
def disp_delete_page():
	return render_template('delete.html')

@app.route('/updatecore')
def disp_update():
	return render_template('update_core.html')

@app.route('/updatemember')
def disp_member():
	return render_template('update_member.html')

@app.route('/viewteam')
def disp_team():
	return render_template('team.html')

@app.route('/bookhub')
def disp_bookhub_page():
	return render_template('books.html')

@app.route('/insert_books')
def disp_insertBooks_page():
	return render_template('Insert_books.html')

@app.route('/buybooks')
def disp_buy_books():
	return render_template('buy_books.html')

@app.route('/logout')
def logouT():
	
	global who_is_it

	who_is_it = None
	return render_template('login.html')

@app.route('/booksindemand')
def disp_books_in_demand():

	data = select_books_in_demand()
	
	return render_template('books_in_demand.html', result = data)

@app.route('/search', methods = ['POST', 'GET'])
def search():

	if(request.method == 'POST'):
		usn = request.form['search']

		data = select_one_student(usn)

		if(data != -1):
			return render_template('view_members.html', result = data)
		else:
			d = select_all_students()
			return render_template('view_members.html', result = d)

@app.route('/searchcore', methods = ['POST', 'GET'])
def searchc():

	if(request.method == 'POST'):
		usn = request.form['searchc']

		data = select_one_core(usn)

		if(data != -1):
			return render_template('view_core.html', result = data)
		else:
			d = select_all_core()
			return render_template('view_core.html', result = d)

@app.route('/searchpod', methods = ['POST', 'GET'])
def searchp():

	if(request.method == 'POST'):
		pod = request.form['searchp']

		data = select_one_pod(pod)

		if(data != -1):
			return render_template('view_core.html', result = data)
		else:
			d = select_all_core()
			return render_template('view_core.html', result = d)	


@app.route('/searchbooks', methods = ['POST', 'GET'])
def searchb():

	if(request.method == 'POST'):
		usn = request.form['searchb']

		data = select_one_book(usn)

		if(data != -1):
			return render_template('view_books.html', result = data)
		else:
			d = select_all_books()
			return render_template('view_books.html', result = d)


@app.route('/searchbooksind', methods = ['POST', 'GET'])
def searchbind():

	if(request.method == 'POST'):
		usn = request.form['searchbind']

		data = select_one_bookind(usn)

		if(data != -1):
			return render_template('books_in_demand.html', result = data)
		else:
			d = select_books_in_demand()
			return render_template('books_in_demand.html', result = d)

# getting the details of a student from a form (in the html)
# and using those details to render a template that dynamically displays the details in a page
# the url in the login.html is of the form <form action = "http://localhost:5000/details" method = "POST">
# this url specifies where to go. for now, it points to the details page and hence, when the user clicks on submit, the details page is rendered. 
# if this url is of the form "http://localhost:5000/login", then it goes to the login page described by the login function that is given below. 
@app.route('/verify', methods = ['POST', 'GET'])
def details():

	global who_is_it

	if request.method == 'POST':
		user = request.form['usn']
		password = request.form['pass']
		who = check_login(user, password)

		if(who == 'User'):
			who_is_it = 'U'
		elif(who == 'Core'):
			who_is_it = 'C'
		elif(who == 'Office'):
			who_is_it = 'O'

		else:
			who_is_it = 'N'
			return render_template('verify.html', user = 'Invalid Username or password')

		return render_template('home.html', user = who)

# create and display the graph.
@app.route('/graph')
def disp_graph():

	data = group_students_by_branch()
	val = []
	names = []

	for r in data:
		val.append(r[0])

	for r in data:
		names.append(r[1])

	print(val, names)	
	plt.subplot(121)
	plt.bar(x = names, height = val, width = 0.2, align = 'center', color = 'g')
	plt.title('Students Grouped by Branch')

	data1 = group_students_by_year()
	val1 = []
	names1 = []

	for r in data1:
		val1.append(r[0])

	for r in data1:
		names1.append(r[1])

	plt.subplot(122)
	val1.sort(reverse = True)
	plt.bar(x = names1, height = val1, width = 0.2, align = 'center', color = 'r')
	plt.title('Students Grouped by Years')
	
	plt.savefig('./static/graph.png')


	return render_template('graph.html')

'''
--------------------------------------------------------------------------------------------------------------------
insert, delete and update operations. 
'''
@app.route('/UpdateCoreForm', methods = ['POST', 'GET'])
def update_core_form():

	if(request.method == 'POST'):
		name = request.form['name']
		usn = request.form['usn']
		year = request.form['year']
		branch = request.form['branch']
		sem = request.form['semester']
		pod = request.form['pod']

		if(who_is_it == 'U' or who_is_it == 'C'):
			return render_template('cannot_delete.html')
		else:

			update_core_query(usn, name, year, sem, branch, pod)
			return render_template('home.html')

@app.route('/UpdateMemberForm', methods = ['POST', 'GET'])
def update_member_form():

	if(request.method == 'POST'):
		name = request.form['name']
		usn = request.form['usn']
		year = request.form['year']
		branch = request.form['branch']
		sem = request.form['semester']
		no_events = request.form['number_of_events_attended']
		no_of_comps = request.form['number_of_competitions']


		if(who_is_it == 'U'):
			return render_template('cannot_delete.html')
		else:
			
			update_member_query(usn, name, year, sem, branch, no_events, no_of_comps)
			
			return render_template('home.html')

@app.route('/deletemember', methods = ['POST', 'GET'])
def delete_member():

	if(request.method == 'POST'):
		usn_st = request.form['usn_delete']

		if(who_is_it == 'U'):
			return render_template('cannot_delete.html')

		delete_st(usn_st)

	return render_template('home.html')

@app.route('/InsertMembersForm', methods = ['POST', 'GET'])
def insert_members_form():

	if(request.method == 'POST'):

		if(who_is_it == 'U'):
			return render_template('cannot_delete.html')

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

		if(who_is_it == 'U' or who_is_it == 'C'):
			return render_template('cannot_delete.html')

		name = request.form['name']
		usn = request.form['usn']
		year = request.form['year']
		branch = request.form['branch']
		sem = request.form['semester']
		pod = request.form['pod']

		insert_core(usn, name, year, sem, branch, pod)

		return render_template('home.html')

@app.route('/InsertBooksForm', methods = ['POST', 'GET'])
def insert_books_form():

	if(request.method == 'POST'):

		if(who_is_it == 'U' or who_is_it == 'C'):
			return render_template('cannot_delete.html')

		book_name = request.form['name']
		author = request.form['author']
		stream = request.form['stream']
		cost = request.form['cost']
		quantity = request.form['quantity']
		usn = request.form['usn']

		insert_books(book_name, author, stream, cost, quantity, usn)

		return render_template('home.html')

@app.route('/buybooks_verify', methods = ['POST', 'GET'])
def buy_books_function():

	if(request.method == 'POST'):

		id = request.form['id'] 

		temp = buy_books(id)

		if(temp == True):
			return render_template('home.html')
		else:
			return render_template('home.html')
			print('No books available')

'''
-------------------------------------------------------------------------------------------------------------------------
Dynamically displaying the contents of the tables using templates in Flask to return the data to the HTML file.
'''

@app.route('/viewoffice')
def view_office():

	conn, cur = connect()
	data = select_all_office()

	return render_template('view_office.html', result = data)

@app.route('/viewcore')
def view_core():

	conn, cur = connect()
	data = select_all_core()

	return render_template('view_core.html', result = data)

@app.route('/viewmembers')
def view_mem():

	conn, cur = connect()
	data = select_all_students()

	return render_template('view_members.html', result = data,)

@app.route('/viewbooks')
def disp_books():
	conn, cur = connect()
	data = show_books_view()

	return render_template('view_books.html', result = data)

@app.route('/viewstudentbooks')
def disp_books_with_students():
	conn, cur = connect()
	data = join_books_and_students()

	return render_template('view_noOf_students_withbooks.html', result = data)


if __name__ == '__main__':
	
	app.secret_key = 'super secret key'

	app.debug = True # debug is used for developing since it allows us to make changes in the python file without having to restart the server again and again.
	app.run()

	disp_graph()