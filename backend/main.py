from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import subprocess
import csv
from datetime import datetime
import os

app = FastAPI()

# CORS Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseItem(BaseModel):
    description: str
    date: str
    cost: float


class Expenses(BaseModel):
    expenses: List[ExpenseItem]
    user_ids: str
    user_shares: str


def reformateDate(date: str) -> str:
    old_datestring = datetime.strptime(date, "%Y-%m-%d")
    return datetime.strftime(old_datestring, "%d.%m.%Y")


@app.post("/upload-data/")
async def upload_data(expenses: Expenses):
    # CSV-Dateiname definieren
    temp_filename = "expenses.csv"

    # CSV-Datei aus den eingegebenen Daten erstellen
    try:
        with open(temp_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["cost", "description", "date"])
            for expense in expenses.expenses:
                writer.writerow([expense.cost, expense.description, reformateDate(expense.date)])

        # Pfad zu Ihrem Python-Skript (anpassen)
        path_to_script = f"{os.path.dirname(os.path.dirname(__file__))}/main.py"  # Pfad ggf. anpassen

        # Befehl zum Aufrufen des Python-Skripts mit subprocess
        command = [
            'python', path_to_script,
            '--csv', temp_filename,
            '--user_ids', *expenses.user_ids.split(","),
            '--user_shares', *expenses.user_shares.split(","),
        ]

        print(f'Running command: {" ".join(command)}')

        # Starte das Python-Skript mit den übergebenen Argumenten
        process = subprocess.run(command, capture_output=True, text=True)
        print(f"Return Code: {process.returncode}")
        print(f"Standard Output: {process.stdout}")
        print(f"Standard Error: {process.stderr}")

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=process.stderr)

        return {"message": "Data processed successfully", "output": process.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))