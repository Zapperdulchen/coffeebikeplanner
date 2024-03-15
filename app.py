from flask import Flask, render_template
from database import engine, session_db, Event, Location, Task, Plan, Person

app = Flask(__name__)
session = session_db(engine)

@app.route('/')
def index():
    events = session.query(Event).all()
    tasks = session.query(Task).all()
    plans = session.query(Plan).all()
    return render_template('template.html', events=events, tasks=tasks, plans=plans)

if __name__ == '__main__':
    app.run(debug=True)
