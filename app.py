import locale
import random
import json
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import session as flask_session
from flask_session import Session as flask_Session
from database import engine, session_db, insert_plan, delete_plan, Event, Location, Task, Placeholder, Plan #, Person

app = Flask(__name__)
session = session_db(engine)

# Setzen der lokalen Einstellungen auf Deutsch, um deutsche Namen für Wochentage und Monate zu erhalten
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')  # Anpassung je nach Betriebssystem und Verfügbarkeit

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

@app.template_filter('random_placeholder')
def random_placeholder(task_id):
    placeholders = session.query(Placeholder).filter(Placeholder.task_id == task_id).all()
    if placeholders:
        return random.choice(placeholders).placeholder
    else:
        return "Helfende Hände"

# # Filter zum Jinja2-Umfeld hinzufügen
# app.jinja_env.filters['random_placeholder'] = random_placeholder

# Filter zur Datums- und Zeitformatierung
@app.template_filter('date')
def date(value, format_string):
    if value is None:
        return ""
    return value.strftime(format_string)

# app.jinja_env.filters['custom_date'] = date

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == app_password:
            flask_session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Falsches Passwort!'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    flask_session.pop('logged_in', None)  # Löschen der Session-Information
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    global session

    events = session.query(Event).all()
    tasks = session.query(Task).all()
    return render_template('plan_events_template.html', events=events, tasks=tasks)


@app.route('/update', methods=['POST'])
@login_required
def update():
    global session

    if request.is_json:
        data = request.get_json()
        event_id = data.get('event')
        task_id = data.get('task')
        person = data.get('person')

        print(f'Received {data}') # DBG

        if person:
            plan_id = insert_plan(session, event_id, person, task_id)
            # Eine Bestätigung zurücksenden
            return jsonify({"message": "Daten erfolgreich aktualisiert" if plan_id else "Keine Änderung an der Datenbank",
                            "plan": plan_id,
                            "event": event_id,
                            "task": task_id,
                            "person": person}), 200
        else:
            plan_id = delete_plan(session, event_id, task_id)
            return jsonify({"message": "Daten erfolgreich gelöscht" if plan_id else "Keine Änderung an der Datenbank",
                            "plan": plan_id,
                            "event": event_id,
                            "task": task_id}), 200
    else:
        return jsonify({"error": "Request body must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True)




