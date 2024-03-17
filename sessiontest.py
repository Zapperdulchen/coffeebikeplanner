import json
from functools import wraps
from flask import Flask, request, redirect, url_for, render_template
from flask import session as flask_session
from flask_session import Session as flask_Session


app = Flask(__name__)

# Konfigurationsdaten aus der JSON-Datei laden
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

app.secret_key = config_data['app_secret_key']
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Ihr Passwort für die Anmeldelogik
app_password = config_data['app_password']

flask_Session(app)

# decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not flask_session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == app_password:
            flask_session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Falsches Passwort!'
    return render_template('login.html')

@app.route('/')
@login_required
def home():
    return 'Willkommen! Sie sind jetzt eingeloggt.'

@app.route('/logout')
@login_required
def logout():
    flask_session.pop('logged_in', None)  # Löschen der Session-Information
    return redirect(url_for('login'))

@app.route('/ok')
@login_required
def ok():
   return 'OKOKOKOKO'

if __name__ == '__main__':
    app.run(debug=True)

