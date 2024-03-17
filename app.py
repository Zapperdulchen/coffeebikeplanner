import locale
import random
from flask import Flask, render_template, request, jsonify
from database import engine, session_db, insert_plan, delete_plan, Event, Location, Task, Placeholder, Plan #, Person

app = Flask(__name__)
session = session_db(engine)

# Setzen der lokalen Einstellungen auf Deutsch, um deutsche Namen für Wochentage und Monate zu erhalten
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')  # Anpassung je nach Betriebssystem und Verfügbarkeit

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

@app.route('/')
def index():
    global session

    events = session.query(Event).all()
    tasks = session.query(Task).all()
    return render_template('plan_events_template.html', events=events, tasks=tasks)


@app.route('/update', methods=['POST'])
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




