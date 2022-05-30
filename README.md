# Gruppe 04 - Aufgabenblatt 2

## 1. Aufgabe

Nachdem das Repo gecloned wurde, empfehlen wir im Projekt-Ordner eine Virtual Environment zu generieren.

     python3 -m venv venv

Daraufhin muss die Virtual Environment zunächst aktiviert werden.

    . venv/bin/activate

Nun müssen die Requirements installiert werden.

    pip install -r requirements.txt

Um die Datenbankverbindung gewährleisten zu können, muss zunächst noch der SUPABASE_KEY gesetzt werden.
Dieser befindet sich in der Abgabe in der Datei SUPABASE_KEY.txt und muss in die Zeile 8 der Datei app.py eingefügt werden.

Zu gu­ter Letzt kann die App gestartet werden.

    python app.py
