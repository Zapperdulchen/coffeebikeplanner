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
        element.setAttribute('contenteditable', 'false');
        event.preventDefault();
        // Überprüft, ob das Element leer ist, und stellt den Platzhalter wieder her
        if (!element.innerText.trim()) {
          element.classList.add('placeholder');
          element.innerText = element.getAttribute('data-placeholder');
        }
        else {
          // Nach dem Beenden der Bearbeitung die Daten an den Server senden
          // sendDataToServer(element.dataset.id, element.innerText);
          console.log(element.dataset.id, element.innerText)
        }
        // Entfernt den Event-Listener, um Leistungsprobleme zu vermeiden
        element.onblur = null;
      }
    };

    // Fügt einen Event-Listener hinzu, um den Platzhalter wiederherzustellen, wenn der Benutzer das Element verlässt
    element.onblur = function() {
      element.setAttribute('contenteditable', 'false');
      if (!element.innerText.trim()) {
        element.classList.add('placeholder');
        element.innerText = element.getAttribute('data-placeholder');
      }
    };
  }

  function sendDataToServer(elementId, text) {
    const url = 'https://example.de/update';
    const data = { id: elementId, text: text };

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
