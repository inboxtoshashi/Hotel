from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

roomlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
customerlist = [{'name': 'Shashi Kant Singh', 'days': '1', 'mobnumber': '1', 'mailid': '1', 'password': '1', 'roomnumber' : '1'}]


app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_PORT']= 3306
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'shashi'
app.config['MYSQL_DB']= 'Hotel'

interface = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	customerlist = interface.connection.cursor()
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('booking.html', value=mail ,output=" has been recorded")
	else:
		return render_template('booking.html')

@app.route('/booking', methods= ['GET', 'POST'])
def booking():
	cursor = interface.connection.cursor()
	global roomnumber
	global roomlist
	global customerlist
	roomcharges = 2000
	totalcharges=0
	if request.method == 'POST':
		mailid = request.form['mailid']
		flag=0
		for room in range(len(roomlist)):
			if roomlist[room] ==0:
				flag=3
				try:
					for user in customerlist:
						if user['mailid'] == mailid:
							flag=2
							break
				except:
					print('Something went wrong')
				if flag == 3:
					name = request.form['name']
					password = request.form['password']
					mobnumber = request.form['mobnumber']
					days = request.form['days']
					roomnumber=room
					roomlist[room]=1

					totalcharges = days*roomcharges


					userdata = {'name' : name, 'mailid' : mailid, 'password' : password,\
								'mobnumber' : mobnumber, 'days' : days, 'roomnumber' : roomnumber}
					customerlist.append(userdata)
					return render_template('booking.html', output=customerlist)
			else:
				pass
		if flag==0:
			return render_template('booking.html', output='Sorry Rooms are not availabel')
		elif flag==2:
			return render_template('booking.html', output='Sorry this ID is already Exist.')

	else:
		return render_template('booking.html',output=' ')

@app.route('/check', methods= ['GET', 'POST'])
def checking():
	cursor = interface.connection.cursor()
	global roomlist
	global customerlist
	if request.method == 'POST':
		flag=0
		mailid = request.form['mailid']
		password = request.form['password']
		for user in customerlist:
			if mailid == user['mailid'] and password == user['password']:
				flag=1
				return render_template('details.html', confirmation=user)
		if flag==0:
			return render_template("roomcheck.html", confirmation = 'Sorry ID or password does not matched.')

	else:
		return render_template('roomcheck.html', output='')

@app.route('/cancel', methods= ['GET', 'POST'])
def cancellation():
	cursor = interface.connection.cursor()
	if request.method == 'POST':
		global roomlist
		global customerlist
		flag=0
		mailid = request.form['mailid']
		password = request.form['password']

		for user in range(len(customerlist) ):
			if mailid == customerlist[user]['mailid'] and password == customerlist[user]['password']:
				flag=1
				data = customerlist[user]
				roomlist[customerlist[user]['roomnumber']]=0
				del customerlist[user]
				return render_template('canceldetails.html', confirmation=data)
			else:
				pass
		if flag==0:
			return render_template('roomcancel.html', confirmation= "ID or Password does not matched.")

	else:
		return render_template('roomcancel.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('about.html', value=mail ,output=" has been recorded")
	else:
		return render_template('about.html')


@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('rooms.html', value=mail ,output=" has been recorded")
	else:
		return render_template('rooms.html')


@app.route('/option', methods=['GET', 'POST'])
def option():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('option.html', value=mail ,output=" has been recorded")
	else:
		return render_template('option.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('contact.html', value=mail ,output=" has been recorded")
	else:
		return render_template('contact.html')


if __name__=='__main__':
	app.run(port=5050)