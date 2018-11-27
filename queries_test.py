import sqlite3


'''
Create Statements
'''
def create_db():

	conn, cur = connect()

	#creating tables in the database
	cur.execute("CREATE TABLE students(usn varchar(11) primary key, name varchar(20), year int, sem int, branch varchar(20), no_of_events int, no_of_wins int)")
	cur.execute("insert into students values(?, ?, ?, ?, ?, ?, ?)", ["4ni16cs003", 'adith', 2016, 5, 'CS', 1, 0])

	cur.execute("CREATE TABLE core(usn varchar(11) primary key, name varchar(20), year int, sem int, branch varchar(20), pod varchar(20))")
	cur.execute("insert into core values(?, ?, ?, ?, ?, ?)", ["4ni16cs025", 'bindu', 2016, 5, 'CS', 'Marketing'])

	cur.execute("CREATE TABLE office(usn varchar(11) primary key, name varchar(20), year int, sem int, branch varchar(20), designation varchar(20))")
	cur.execute("insert into office values(?, ?, ?, ?, ?, ?)", ["4ni16cs010", 'akshat', 2016, 5, 'CS', 'Secretary'])

	cur.execute("CREATE TABLE events(eventID int, name varchar(20), event_date date, venue varchar(20), concept varchar(20))")
	cur.execute("insert into events values(?, ?, ?, ?, ?)", [1, 'Rags to Riches', '2018-09-08', 'M.V hall', 'Idea Generation'])

	conn.commit()

def create_bookhub_database():

	conn, cur = connect()

	cur.execute('''CREATE TABLE bookhub(id integer primary key autoincrement default 1, book_name varchar(20), author varchar(20), stream varchar(10), 
				cost int, quantity int, sold_price int, usn varchar(10), foreign key(usn) references students(usn) )''')

	conn.commit()
	conn.close()

def create_inDemand_table():

	conn, cur = connect()

	cur.execute('''CREATE TABLE in_demand(id integer , book_name varchar(20), author varchar(20), stream varchar(10), 
				cost int, quantity int, sold_price int, usn varchar(10) )''')

	conn.commit()
	conn.close()

def connect():

	conn = sqlite3.connect("./onyx.db")
	cur = conn.cursor()

	return conn, cur

'''
------------------------------------------------------------------------------------------------------
Insert queries:

'''
def insert_student(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', no_events= 'null', no_wins = 'null'):

	conn, cur = connect()
	cur.execute('insert into students values(?, ?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, no_events, no_wins])
	conn.commit()
	conn.close()

def insert_event(e_id = 'null', name = 'null', date = 'null', venue='null' , concept = 'null'):

	conn, cur = connect()
	cur.execute('insert into events values(?, ?, ?, ?, ?)', [e_id, name, date, venue, concept])
	conn.commit()
	conn.close()

def insert_core(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', pod= 'null'):

	conn, cur = connect()
	cur.execute('insert into core values(?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, pod])
	conn.commit()
	conn.close()

def insert_office(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', designation = 'null'):

	conn, cur = connect()
	cur.execute('insert into office values(?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, designation])
	conn.commit()
	conn.close()

def insert_books(book_name = 'null', author ='null', stream = 'null', cost='null', quantity='null', sold_price='null', usn='null'):

	conn, cur = connect()
	cur.execute('insert into bookhub(book_name, author, stream, cost, quantity, sold_price, usn) values(?, ?, ?, ?, ?, ?, ?)', [book_name, author, stream, cost, quantity, sold_price, usn])
	conn.commit()
	conn.close()	

'''
----------------------------------------------------------------------------------------

Update Queries
'''

def update_member_query(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', no_events= 'null', no_wins = 'null'):

	conn, cur = connect()
	cur.execute('update students set name = ?, year = ?, sem = ?, branch = ?, no_of_events = ?, no_of_wins = ? where usn = ?', [name, year, sem, branch, no_events, no_wins, usn])
	conn.commit()
	conn.close()

def update_core_query(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', pod= 'null'):

	conn, cur = connect()
	cur.execute('update core set name = ?, year = ?, sem = ?, branch = ?, pod = ? where usn = ?', [name, year, sem, branch, pod, usn])
	conn.commit()
	conn.close()

# basically update the bookhub table and decrement quantity.
def buy_books(id):

	conn, cur = connect()
	cur.execute('select * from bookhub where id = ?', (id, ))
	data = cur.fetchall()

	if(data):
		cur.execute('update bookhub set quantity = quantity - 1 where id = ?', (id, ))
		conn.commit()
		return True

	else:
		return False


'''
------------------------------------------------------------------------------------------------------

selection queries:

'''

def select_one_student(usn):

	conn, cur = connect()
	cur.execute('select * from students where name like ?', ('%'+usn+'%', ))

	data = cur.fetchall()
	conn.close()

	if(data):
		return data
	else:
		return -1

def select_one_core(usn):

	conn, cur = connect()
	cur.execute('select * from core where name like ?', ('%'+usn+'%', ))

	data = cur.fetchall()
	conn.close()

	if(data):
		return data
	else:
		return -1

def select_one_pod(pod):

	conn, cur = connect()
	cur.execute('select * from core where pod like ?', ('%'+pod+'%', ))

	data = cur.fetchall()
	conn.close()

	if(data):
		return data
	else:
		return -1

def select_one_book(name):

	conn, cur = connect()
	cur.execute('select * from bookhub where book_name like ?', ('%'+name+'%', ))

	data = cur.fetchall()
	conn.close()

	if(data):
		return data
	else:
		return -1

def select_one_bookind(name):

	conn, cur = connect()
	cur.execute('select * from in_demand where book_name like ?', ('%'+name+'%', ))

	data = cur.fetchall()
	conn.close()

	if(data):
		return data
	else:
		return -1

def select_all_events():

	conn, cur = connect()
	cur.execute('select * from events')

	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data

def select_all_students():

	conn, cur = connect()
	cur.execute('select * from students')

	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data

def select_all_core():

	conn, cur = connect()
	cur.execute('select * from core')

	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data	

def select_all_office():

	conn, cur = connect()
	cur.execute('select * from office')

	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data	

def select_all_books():

	conn, cur = connect()
	cur.execute('select * from bookhub')

	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data

def select_books_in_demand():

	conn, cur = connect()
	cur.execute('select * from in_demand')

	data = cur.fetchall()
	conn.close()

	return data

'''
------------------------------------------------------------------------------------------------------------------
Group Queries
'''

def group_students_by_branch():

	conn, cur = connect()

	cur.execute("select count(*) as count_branch, branch from students group by branch order by count_branch desc")
	data = cur.fetchall()
	
	for r in data:
		print(r)

	return data


def group_students_by_year():

	conn, cur = connect()

	cur.execute("select count(*) as count_year, year from students group by year order by count_year desc")
	data = cur.fetchall()
	
	for r in data:
		print(r)

	return data

'''
delete if he/she exists in the database.
if the usn belongs to students table, delete from students
else if it belongs to core, delete from core
else if it belongs to office bearers, delete from that.
else it doesnt belong to any table. (not a member)
'''
def delete_st(usn):
	
	conn, cur = connect()
	cur.execute('select * from students where usn=?', (usn, ))
	d = cur.fetchall()

	if(d):
		cur.execute('delete from students where usn = ?', (usn, ))
	else:
		cur.execute('select * from core where usn=?', (usn, ))
		d = cur.fetchall()

		if(d):
			cur.execute('delete from core where usn = ?', (usn, ))
		else:
			cur.execute('select * from office where usn=?', (usn, ))
			d = cur.fetchall()

			if(d):
				cur.execute('delete from office where usn = ?', (usn, ))

			else:
				print('invalid usn')

	conn.commit()

	#select_all_students()

'''
Authenticating the user and checking to see if the usn exists in the database or not.
'''
def check_login(usn, password):

	conn, cur = connect()

	cur.execute("select * from students where usn=?", (str(usn), ))
	data = cur.fetchall()

	if(data):
		return 'User'

	else:
		cur.execute("select * from core where usn=?", (str(usn), ))
		data1 = cur.fetchall()

		if(data1 and password == 'core'):
			return 'Core'
		else:
			cur.execute("select * from office where usn=?", (str(usn), ))
			data2 = cur.fetchall()

			if(data2 and password == 'office'):
				return 'Office'
			else:
				return 'Not'

	conn.close()

'''
Joining students and books table to get the students who have sold the book.
Used Natural Join to eliminate usn appearing twice in the result. 
'''

def join_books_and_students():

	conn, cur = connect()

	cur.execute("select * from students natural join bookhub where students.usn = bookhub.usn order by year")
	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data

'''
-----------------------------------------------------------------------------------------------------------------
Views
'''

def create_books_view():

	conn, cur = connect()

	cur.execute('''CREATE VIEW show_books as SELECT 
					id,
					book_name,
					author,
					stream,
					cost,
					quantity
					from bookhub;''')

	conn.commit()
	conn.close()

def show_books_view():

	conn, cur = connect()

	cur.execute('SELECT * from show_books')
	data = cur.fetchall()
	conn.close()

	for r in data:
		print(r)

	return data

'''
---------------------------------------------------------------------------------------------------------------------
Triggers
'''

def create_trigger():

	conn, cur = connect()

	cur.execute('''CREATE trigger add_books_to_inDemand 
				   
				   after UPDATE 
				   on bookhub
				   WHEN NEW.quantity == 0
				   
				   BEGIN	 

				   		insert into in_demand values(new.id, new.book_name, new.author, 
				   		new.stream, new.cost, new.quantity, new.sold_price, new.usn);

				   		delete from bookhub where id = new.id;

				   END;

				''')

	conn.commit()
	conn.close()

select_all_students()
print('-----')
select_all_core()
print('-----')
select_all_office()
print('------')
select_all_events()
print('------')
select_all_books()
print('----------')
join_books_and_students()
select_all_students() 
select_all_books()


