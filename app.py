import locale
from flask import Flask, render_template, request, jsonify
from database import engine, session_db, insert_plan, Event, Location, Task, Plan #, Person

app = Flask(__name__)
session = session_db(engine)

# Setzen der lokalen Einstellungen auf Deutsch, um deutsche Namen für Wochentage und Monate zu erhalten
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')  # Anpassung je nach Betriebssystem und Verfügbarkeit

# Filter zur Datums- und Zeitformatierung
@app.template_filter('date')
def date(value, format_string):
    if value is None:
        return ""
    return value.strftime(format_string)

app.jinja_env.filters['custom_date'] = date

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

        plan_id = insert_plan(session, event_id, person, task_id)

        # Eine Bestätigung zurücksenden
        return jsonify({"message": "Daten erfolgreich aktualisiert",
                        "plan": plan_id,
                        "event": event_id,
                        "task": task_id,
                        "person": person}), 200
    else:
        return jsonify({"error": "Request body must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True)




