from flask import (
	Flask,
	render_template,
	request,
	redirect,
	url_for,
	Blueprint
)
from flaskext.mysql import MySQL
app = Flask(__name__)

logged_in = 0

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aditya'
app.config['MYSQL_DATABASE_DB'] = 'metro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#app = Blueprint('metro', __name__)

# @app.route('/')
# def home():
# 	return redirect('/metro')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/info/')
def info():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT distinct sname from metro_facility order by sname")
	data = cursor.fetchall()
	return render_template('info.html',data=data)

@app.route('/directions/')
def directions():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT distinct sname from metro_facility order by sname")
	data = cursor.fetchall()
	return render_template('directions.html',data=data)

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/review/')
def review():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT distinct sname from metro_facility order by sname")
	data = cursor.fetchall()
	return render_template('review.html',data=data)

@app.route('/review2/')
def review2():
	name = request.args.get('stat_name')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT title,bodytext,author from reviews where sname = '"+ name +"' and approval = 'Yes'")
	review = cursor.fetchall()
	return render_template('review2.html',review=review)

@app.route('/add_rev',methods=['GET','POST'])
def add():
	data = "Error, please try again"
	if request.method == 'POST':
		stat = request.form['stat']
		title = request.form['title']
		desc = request.form['desc']
		author = request.form['author']
		cursor = mysql.connect().cursor()
		cursor.execute("insert into reviews(sname,title,author,timest,bodytext,approval) values ('"+ stat + "','" + title + "','" + author + "', now() ,'" + desc + "','No')")
		cursor.execute('COMMIT')
		data = "Review has been added. It will be displayed once approved by the admin."
	return render_template('boilerplate.html',data=data)

@app.route('/directions2')
def dir_actual():
	source = request.args.get('source')
	dest = request.args.get('dest')
	cursor = mysql.connect().cursor()
	cursor.execute("CALL find_path('"+ source +"','"+ dest +"')")
	data = cursor.fetchall()
	return render_template('directions2.html',data=data,source=source,dest=dest)

@app.route('/info2')
def info_actual():
	name = request.args.get('stat_name')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from metro_facility where sname = '" + name + "'")
	infor = cursor.fetchone()
	cursor.execute("SELECT line,grade from metro_stations where sname = '" + name + "'")
	inform = cursor.fetchall()
	cursor.execute("SELECT place from metro_places where sname = '" + name + "'")
	informa = cursor.fetchall()
	return render_template('info2.html',infor=infor,inform=inform,informa=informa)

@app.route('/nearest/<info>')
def closer(info):
	if info == 'pin':
		pincode = request.args.get('code')
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT sname from metro_facility where pincode = '"+ pincode +"'")
		stations = cursor.fetchall()
		return render_template('nearest2.html',stations=stations)
	if info == 'near':
		place = request.args.get('by')
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT sname from metro_places where place = '" + place +"'")
		stations = cursor.fetchall()
		return render_template('nearest2.html',stations=stations)
	return render_template('nearest.html')


@app.route('/admin')
def admin():
	data = "You are not logged in. Please log in to access admin features."
	if logged_in == 1:
		return render_template('admin.html')
	return render_template("boilerplate.html", data=data)

@app.route('/addadmin', methods=['POST','GET'])
def addadmin():
	data = "You aren't logged in as admin yet. Please login first."
	if request.method == 'POST':
		cursor = mysql.connect().cursor()
		user = request.form['user']
		passw = request.form['passa']
		passo = request.form['passb']
		if passo == passw:
			cursor.execute("Select count(*) from metro_admin where username = '" + user + "'")
			username = cursor.fetchone()
			if username == user:
				data = "Username already exists, please try again."
			else:
				cursor.execute("insert into metro_admin values ('" + user + "','" + passw + "')")
				cursor.execute('COMMIT')
				data = "Admin added successfully"
		else:
			data = "Passwords dont match, please try again."
	return render_template("boilerplate.html",data=data)

@app.route('/deladmin',methods=['GET','POST'])
def adderall():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "Please access page through proper channel."
		if request.method == 'POST':
			data = "Password is incorrect."
			user = requesst.form['usera']
			passw = request.form['passa']
			cursor = mysql.connect().cursor()
			cursor.execute("SELECT count(*) from metro_admin where password='" + passw + "' and username='"+ user +"'")
			counter = cursor.fetchone()
			if counter[0] == 1:
				data = "Admin removed successfully."
				cursor.execute("DELETE from metro_admin where password='" + passw + "' and username ='" +user+ "'")
				cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/addmin')
def adder():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		return render_template('addmin.html')
	return render_template('boilerplate.html',data=data)

@app.route('/addstation')
def stati():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT distinct sname from metro_stations")
		data = cursor.fetchall()
		return render_template('addstation.html',data=data)
	return render_template('boilerplate.html',data=data)

@app.route('/editinfo')
def infoedit():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT distinct sname from metro_facility order by sname")
		data = cursor.fetchall()
		return render_template('editinfo.html',data=data)
	return render_template('boilerplate.html',data=data)

@app.route('/editinfo2',methods=['GET','POST'])
def infoedit2():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "More data required. Please try again."
		if request.method == 'POST':
			data = "Station values edited successfully!"
			cursor = mysql.connect().cursor()
			oldname = request.form['stat_name']
			newname = request.form['sname']
			date = request.form['date']
			pin = request.form['pin']
			contact = request.form['contact']
			washroom = request.form['washroom']
			parking = request.form['parking']
			elevator = request.form['elevator']
			cursor.execute("update metro_facility set sname='" +newname+ "',washroom='" +washroom+ "',parking= '" +parking+ "',elevator= '" +elevator+ "',opening_date= '" +date+ "',contact= '"+contact+"' where sname='"+oldname+"'")
			cursor.execute("update metro_stations set sname='"+newname+"' where sname='"+oldname+"'")
			cursor.execute("update metro_places set sname='" +newname+ "' where sname='"+oldname+"'")
			cursor.execute("update reviews set sname='" +newname+ "' where sname='"+oldname+"'")
			cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/addstat',methods=['POST','GET'])
def addstatic():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "This page requires additional information not posted. Please try again."
		if request.method == 'POST':
			data = "Data has been added successfully."
			sname = request.form['sname']
			sline = request.form['line']
			opdate = request.form['date']
			pin = request.form['pin']
			contact = request.form['contact']
			wash = request.form['washroom']
			park = request.form['parking']
			grade = request.form['grade']
			elev = request.form['elevator']
			adjacent = request.form['adjacent']
			cursor = mysql.connect().cursor()
			cursor.execute("CALL add_station('" + adjacent + "','" + sname + "','" + wash + "','" + park + "','" + elev + "','" + opdate + "','" + contact + "','" + pin + "', 1 ,'" + sline + "','" + grade + "')")
			cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/re_view')
def rehash():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		x = 1
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * from reviews where approval = 'No' ")
		data = cursor.fetchall()
		return render_template('re_view.html',data=data, x=x)
	return render_template('boilerplate.html',data=data)

@app.route('/authenticate', methods=['POST','GET'])
def login():
	data = "Some error occured while processing your request. Please try again."
	error = None
	if request.method == 'POST':
		user = request.form['InputEmail']
		passw = request.form['InputPassword']
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT count(*) from metro_admin where username='" + user + "' and password='" + passw + "'")
		count = cursor.fetchone()
		if count[0] == 1:
			global logged_in
			logged_in = 1
			return redirect(url_for('admin'))
	return render_template('boilerplate.html',data=data)


@app.route('/re_view2')
def rev():
	riddle = request.args.get('id')
	cursor = mysql.connect().cursor()
	cursor.execute("UPDATE reviews set approval = 'Yes' where timest = '" + riddle + "'")
	cursor.execute('COMMIT')
	return redirect(url_for('rehash'))

@app.route('/re_view3')
def revel():
	riddle = request.args.get('id')
	cursor = mysql.connect().cursor()
	cursor.execute("DELETE from reviews where timest = '" + riddle + "'")
	cursor.execute('COMMIT')
	return redirect(url_for('rehash'))

@app.route('/nearest/')
def trial():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT distinct pincode from metro_facility order by pincode")
	data = cursor.fetchall()
	cursor.execute("SELECT distinct place from metro_places order by place")
	names = cursor.fetchall()
	return render_template('nearest.html',data=data, names=names )

@app.route('/places')
def placate():
	data = "You aren't logged in as admin yet. Please login first."
	if logged_in == 1:
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT distinct place from metro_places order by place")
		data1 = cursor.fetchall()
		cursor.execute("SELECT distinct sname from metro_stations order by sname")
		data2 = cursor.fetchall()
		return render_template('placeadmin.html',data1=data1,data2=data2)
	return render_template('boilerplate.html',data=data)

@app.route('/delplace',methods=['GET','POST'])
def delplace():
	data = "You arent logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "The request wasn't parsed correctly. Please try again."
		if request.method == 'POST':
			data = "Place deleted successfully."
			cursor = mysql.connect().cursor()
			pname = request.form['pname']
			cursor.execute("DELETE from metro_places where place='" + pname + "'")
			cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/editplace',methods=['GET','POST'])
def editplace():
	data = "You arent logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "The request wasn't parsed correctly. Please try again."
		if request.method == 'POST':
			data = "Place edited successfully."
			cursor = mysql.connect().cursor()
			opname = request.form['opname']
			npname = request.form['npname']
			cursor.execute("UPDATE metro_places set place = '" + npname + "' where place='" + opname + "'")
			cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/addplace',methods=['GET','POST'])
def addplace():
	data = "You arent logged in as admin yet. Please login first."
	if logged_in == 1:
		data = "The request wasn't parsed correctly. Please try again."
		if request.method == 'POST':
			data = "Place added successfully."
			cursor = mysql.connect().cursor()
			sname = request.form['sname']
			pname = request.form['pname']
			cursor.execute("INSERT into metro_places(sname,place) values ('" + sname + "','"+pname +"')")
			cursor.execute('COMMIT')
	return render_template('boilerplate.html',data=data)

@app.route('/logout')
def logout():
	global logged_in
	logged_in = 0
	data = "You have been logged out successfully"
	return render_template('boilerplate.html',data=data)


if __name__ == '__main__':
	app.debug = True
	# app.register_blueprint(app, url_prefix='/metro')
	#app.register_blueprint(app, url_prefix='/')
	app.run(host='0.0.0.0')
