function makeEditable(element) {
    // Entfernt den Platzhalterstil, wenn der Benutzer mit der Bearbeitung beginnt
    if (element.classList.contains('placeholder')) {
        element.classList.remove('placeholder');
        if (element.innerText === element.getAttribute('data-placeholder')) {
            element.innerText = '';
        }
    }

    element.setAttribute('contenteditable', 'true');
    element.focus();

    element.onkeydown = function(event) {
        if (event.key === 'Enter') {
            element.blur(); // Veranlasst das 'blur'-Ereignis, was das Element deselektiert
            event.preventDefault(); // Verhindert einen Zeilenumbruch
        }
        // TODO - pressing ESC restores old value
    };

    element.onblur = function() {
        element.setAttribute('contenteditable', 'false');
        // Überprüft, ob das Element leer ist, und stellt den Platzhalter wieder her
        if (!element.innerText.trim()) {
            element.classList.add('placeholder');
            element.innerText = element.getAttribute('data-placeholder');
        } else {
            // Nach dem Beenden der Bearbeitung die Daten an den Server senden
            sendDataToServer(element.dataset.event, element.dataset.task, element.innerText.trim());
            console.log(element.dataset.event, element.dataset.task, element.innerText.trim())
        }
    };
}

function sendDataToServer(eventId, taskId, text) {
    const url = '/update';
    const data = {
        event: eventId,
        task: taskId,
        person: text
    };

    fetch(url, {
            method: 'POST', // oder 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
