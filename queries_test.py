import sqlite3

def create_db():


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


def connect():

	conn = sqlite3.connect("./onyx.db")
	cur = conn.cursor()

	return conn, cur


def insert_student(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', no_events= 'null', no_wins = 'null'):

	conn, cur = connect()
	cur.execute('insert into students values(?, ?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, no_events, no_wins])
	conn.commit()
	conn.close()

	select_all_students()

def insert_event(e_id = 'null', name = 'null', date = 'null', venue='null' , concept = 'null'):

	conn, cur = connect()
	cur.execute('insert into events values(?, ?, ?, ?, ?)', [e_id, name, date, venue, concept])
	conn.commit()
	conn.close()

	select_all_events()

def insert_core(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', pod= 'null'):

	conn, cur = connect()
	cur.execute('insert into core values(?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, pod])
	conn.commit()
	conn.close()

	select_all_core()

def insert_office(usn = 'null', name = 'null', year = 'null', sem='null' , branch = 'null', designation = 'null'):

	conn, cur = connect()
	cur.execute('insert into office values(?, ?, ?, ?, ?, ?)', [usn, name, year, sem, branch, designation])
	conn.commit()
	conn.close()

	select_all_office()

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

def check_login(usn):

	conn, cur = connect()

	cur.execute("select * from students where usn=?", (str(usn), ))
	data = cur.fetchall()

	if(data):
		return 'User'

	else:
		cur.execute("select * from core where usn=?", (str(usn), ))
		data1 = cur.fetchall()

		if(data1):
			return 'Core'
		else:
			cur.execute("select * from office where usn=?", (str(usn), ))
			data2 = cur.fetchall()

			if(data2):
				return 'Office'
			else:
				return 'Not'

	conn.close()

select_all_students()
print('----')
select_all_office()
print('----')
select_all_core()

