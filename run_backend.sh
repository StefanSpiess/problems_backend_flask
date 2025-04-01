#!/bin/bash

# Stelle sicher, dass wir uns im Verzeichnis des Skripts befinden
cd "$(dirname "$0")"

# Prüfe oder erstelle und aktiviere virtuelle Umgebung
if [ ! -d "venv" ]; then
    echo "⚠️ venv existiert nicht – erstelle neue Umgebung"
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install flask-cors
else
    source venv/bin/activate
fi

# flask-cors vorsichtshalber nochmal sicherstellen
pip list | grep flask-cors > /dev/null || pip install flask-cors

# Starte Flask direkt via python-Befehl (das löst dein Pfad-Problem)
export FLASK_DEBUG=1
python app.py