document.getElementById('expense-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const tableData = [];
    const table = document.getElementById("expenses-table");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        const rowData = {
            description: cells[0].getElementsByTagName("input")[0].value,
            date: cells[1].getElementsByTagName("input")[0].value,
            cost: cells[2].getElementsByTagName("input")[0].value,
        };
        tableData.push(rowData);
    }

    const data = {
        expenses: tableData,
        user_ids: document.getElementById('userIds').value,
        user_shares: document.getElementById('userShares').value,
    };

    // Verwenden Sie die submitData Funktion, um die Daten zu senden
    await submitData(data);
});

function addRow() {
    const table = document.getElementById("expenses-table").getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    // Beschreibungsfeld
    let cell1 = newRow.insertCell(0);
    let descriptionInput = document.createElement("input");
    descriptionInput.type = "text";
    descriptionInput.name = "description";
    descriptionInput.className = "form-control";
    cell1.appendChild(descriptionInput);

    // Datumsfeld
    let cell2 = newRow.insertCell(1);
    let dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.name = "date";
    dateInput.className = "form-control";
    cell2.appendChild(dateInput);

    // Kostenfeld
    let cell3 = newRow.insertCell(2);
    let costInput = document.createElement("input");
    costInput.type = "number";
    costInput.name = "cost";
    costInput.step = "0.01";
    costInput.className = "form-control";
    cell3.appendChild(costInput);

    // Löschen-Knopf
    let cell4 = newRow.insertCell(3);
    let deleteButton = document.createElement("button");
    deleteButton.className = "btn btn-danger";
    deleteButton.textContent = "X";
    deleteButton.onclick = function() {
        // Überprüfen, ob dies die letzte Zeile ist
        if (table.rows.length > 1) {
            this.closest("tr").remove();
        } else {
            // Wenn es die letzte Zeile ist, Felder leeren
            descriptionInput.value = "";
            dateInput.value = "";
            costInput.value = "";
        }
    };
    cell4.appendChild(deleteButton);
}

function displayResponse(message) {
    document.getElementById('response').innerText = message;
}

async function submitData(data) {
    // Sicherstellen, dass die Daten korrekt in der Konsole ausgegeben werden
    console.log("Anfragedaten vor dem Senden:", JSON.stringify(data, null, 2));

    try {
        const backendUrl = '/api/upload-data/';
        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Serverantwort:", JSON.stringify(result, null, 2));
        displayResponse(`Erfolg: ${JSON.stringify(result)}`);
    } catch (error) {
        console.error('Fehler beim Senden:', error);
        displayResponse(`Fehler: ${error.toString()}`);
    }
}