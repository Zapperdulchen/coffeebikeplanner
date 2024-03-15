#Caferad Scheduler

##Motivation

Das Caferad in Großgründlach ...

Um für einen Einsatz die Aufgaben zu planen

Wenn es dann sowieso schon eine Webapp gibt, dann soll sie auch gleich zum Anzeigen der Einsatztermine und -orte genutzt werden. (Impressumspflicht?)

##Constraints

- Die Menschen, die die App benutzen werden, sind nicht IT-affin.
- In der Webapp werden zumindest die Namen der anderen Beteiligten sichtbar sein. Daher müssen DSGVO eingehalten werden.
- Weil meine Javascriptkenntnisse minimal sind, soll die App mit Phython + HTML umgesetzt werden.
- Da nicht ausgeschlossen werden, kann das Dritte Zugang zur Website bekommen, sollen Planungsstände im Backend gespeichert werden, um im Falle von Vandalismus auf eine frühere Version zurückgreifen zu können.
- Wenn sich jemand einträgt, der im Backend noch unbekannt ist, soll sie/er einen Hinweis bekommen, dass sie/er sich (per Mail?) anmelden sollen.
- Mehrere gleichzeitige Benutzer können wir erst einmal ausschließen. Dann braucht es aber ein Time-Out. Es wäre prima, wenn ein wartender Benutzer sehen würde, wie lange die App noch gesperrt ist.


##Lösungsidee

- Webframework Flask
- SQLLite für die Speicherung, zu Beginn einfach nur ein Log File
- HTMX - wenn überhaupt 


## Prompt

Gehe davon aus, dass in der DB für Location, Event, Task und Person bereits Werte hinterlegt sind.

Erstelle eine Webapp mit Flask, die in einer tabellarischen Form alle Events auflistet: date, location, task* - wobei bei den task-Spalten der Name der Person angezeigt wird, die sich eingetragen hat. Durch Klicken auf eine Taskzelle kann man die Person ändern.

## Deployment

heroku
pythonanywhere.com
render.com
vercel

ionos.de
