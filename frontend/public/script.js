document.getElementById('expense-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", document.getElementById('csvFile').files[0]);
    formData.append("user_ids", document.getElementById('userIds').value);
    formData.append("user_shares", document.getElementById('userShares').value);

    try {
        // Anpassung: API-Endpunkt entsprechend deiner Backend-Konfiguration setzten
        const response = await fetch('http://127.0.0.1:8000/upload-csv/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Erfolgreiche Antwort verarbeiten
        console.log(result);
        displayResponse(`Erfolg: ${JSON.stringify(result)}`);
    } catch (error) {
        // Fehlerbehandlung
        console.error('Fehler beim Hochladen:', error);
        displayResponse(`Fehler: ${error.toString()}`);
    }
});

// Funktion zum Anzeigen der Response im Frontend
function displayResponse(message) {
    // Stelle sicher, dass ein Element mit der ID "response" im HTML existiert
    document.getElementById('response').innerText = message;
}