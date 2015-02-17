from flask import Flask, render_template, request, jsonify, \
    redirect, url_for, session, send_file
from functools import wraps
import sqlite3
import subprocess
import sql_clients

# creates application object
app = Flask(__name__)

# encrypts sessions
app.secret_key = 'long random string'


# decorator redirects to login page if user is not logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


# renders index.html if logged in
@app.route('/')
@login_required
def home():
    return render_template('index.html')


# checks username / password, returns error, logs user in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        user, password = request.form['username'], request.form['password']
        if len(user) < 20 and len(password) < 20:
            if user != 'test' or password != 'test':
                error = 'Invalid credentials. Please try again.'
            else:
                session.permanent = True
                session['logged_in'] = True
                return redirect(url_for('home'))
        else:
            error = 'Under twenty characters, please.'
    return render_template('login.html', error=error)


# logs user out (deletes session)
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# adds new client to database
@app.route('/addclient', methods=['POST'])
@login_required
def addclient():
    name = request.form['name']
    birthdate = request.form['birthdate']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    citystate = request.form['citystate']
    notes = request.form['notes']
    favoriteline = request.form['favoriteline']
    cabintype = request.form['cabintype']
    diningtime = request.form['diningtime']
    travelswith = request.form['travelswith']
    trips = request.form['trips']
    values = (name, birthdate, email, phone, address, citystate,
              notes, favoriteline, cabintype, diningtime, travelswith, trips)
    try:
        lastid = sql_clients.addclient(values)
        return jsonify(result="Client added successfully.", id=lastid)
    except:
        return jsonify(result="Error adding client.")


# searches for and returns clients matching parameters
@app.route('/clientsearch')
@login_required
def clientsearch():
    query = request.args.get('a')
    value = request.args.get('z')
    with sqlite3.connect('clients.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, citystate FROM clients WHERE " + value +
                  " like \'%"+query+"%\';")
        try:
            result = [dict(id=row[0], name=row[1], citystate=row[2])
                      for row in c.fetchall()]
        except:
            result = "error1"
    return jsonify(result=result)


# returns full client information for specific id
@app.route('/openclient')
@login_required
def openclient():
    clientid = (request.args.get('b'),)
    with sqlite3.connect('clients.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM clients WHERE id=?", clientid)
        try:
            result = [dict(id=row[0], name=row[1], birthdate=row[2],
                    email=row[3], phone=row[4], address=row[5],
                    citystate=row[6], notes=row[7], favoriteline=row[8],
                    cabintype=row[9], diningtime=row[10], travelswith=row[11],
                    trips=row[12]) for row in c.fetchall()]
        except:
            result = "error"
        return jsonify(result=result)


# deletes client
@app.route('/deleteclient')
@login_required
def deleteclient():
    clientid = (request.args.get('id'),)
    with sqlite3.connect('clients.db') as conn:
        c = conn.cursor()
        try:
            c.execute("DELETE FROM clients WHERE id=?", clientid)
            result = "Client deleted."
        except:
            result = "error"
        return jsonify(result=result)


# updates client info
@app.route('/updateclient', methods=['POST'])
@login_required
def updateclient():
    id = request.form['id']
    name = request.form['name']
    birthdate = request.form['birthdate']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    citystate = request.form['citystate']
    notes = request.form['notes']
    favoriteline = request.form['favoriteline']
    cabintype = request.form['cabintype']
    diningtime = request.form['diningtime']
    travelswith = request.form['travelswith']
    trips = request.form['trips']
    values = (name, birthdate, email, phone, address, citystate, notes,
              favoriteline, cabintype, diningtime, travelswith, trips, id)
    sql_clients.updateclient(values)
    return jsonify(result="Client updated successfully.")


# sends database file as attachment
@app.route('/downloaddb')
@login_required
def downloaddb():
    return send_file('clients.db', as_attachment=True)


# converts database to spreadsheet, sends as attachment
@app.route('/dlspreadsheet')
@login_required
def dlspreadsheet():
    subprocess.call('sqlite3 -header -separator "\t" clients.db \'select * '
                    'from clients;\'> clients.csv', shell=True)
    return send_file('clients.csv', as_attachment=True)
