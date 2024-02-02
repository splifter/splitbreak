from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import subprocess
import os
import shutil

app = FastAPI()

# CORS Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-csv/")
async def create_upload_file(
        file: UploadFile = File(...),
        user_ids: str = Form(...),
        user_shares: str = Form(...),
        # Fügen Sie weitere Felder wie benötigt hinzu
        consumer_key: str = Form(None),
        consumer_secret: str = Form(None),
        api_key: str = Form(None),
        group_id: str = Form(None)
):
    # CSV in temporäre Datei speichern
    temp_filename = "temp.csv"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Pfad zu deinem Python-Skript (anpassen)
    path_to_script = "main.py"

    # Linux/Mac: Verwendung von 'python3' könnte erforderlich sein
    command = [
        'python', path_to_script,
        '--csv', temp_filename,
        '--user_ids', *user_ids.split(','),
        '--user_shares', *user_shares.split(','),
    ]

    # Füge zusätzliche Konfigurationen nur hinzu, wenn sie vorhanden sind
    if consumer_key: command.extend(['--consumer_key', consumer_key])
    if consumer_secret: command.extend(['--consumer_secret', consumer_secret])
    if api_key: command.extend(['--api_key', api_key])
    if group_id: command.extend(['--group_id', group_id])

    # Starte das Python-Skript mit den übergebenen Argumenten
    process = subprocess.run(command, capture_output=True, text=True)

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=process.stderr)

    return {"filename": file.filename, "message": "File processed successfully", "output": process.stdout}