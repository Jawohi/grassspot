# GrassSpot

GrassSpot ist eine Web-Applikation zur Verwaltung von Pflanzen in Gärten, die es Benutzern ermöglicht, ein Pflegetagebuch für jede ihrer Pflanzen zu führen. Die Applikation bietet Funktionen wie das Hinzufügen, Bearbeiten, Deaktivieren und Anzeigen von Pflanzendaten sowie das Hochladen von Bildern und das Führen von Pflegetagebüchern.

## Erste Schritte

Diese Anleitung führt Sie durch die Schritte zur Einrichtung des Projekts auf Ihrem lokalen Rechner für Entwicklungs- und Testzwecke.

### Voraussetzungen

Um GrassSpot auf Ihrem System zu installieren, benötigen Sie die folgenden Tools:

- Python 3.8 oder höher
- pip (Python-Paketmanager)
- MongoDB Server oder Zugang zu einer MongoDB-Instanz

### Installation

1. Klonen Sie das Repository auf Ihren lokalen Computer:
   ```bash
   git clone https://github.com/your-username/GrassSpot.git
   cd GrassSpot
   ```

2. Installieren Sie die erforderlichen Python-Pakete:
   ```bash
   pip install -r requirements.txt
   ```

3. Konfigurieren Sie die Umgebungsvariablen, indem Sie eine Datei namens `.flaskenv` im Wurzelverzeichnis des Projekts erstellen. Diese Datei sollte die folgenden Variablen enthalten:
   ```plaintext
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=IhrGeheimerSchlüssel
   MONGO_URI=IhreMongoDBUri
   UPLOADED_PHOTOS_DEST=pfad/zum/speichern/der/bilder
   ```

   Ersetzen Sie `IhrGeheimerSchlüssel` und `IhreMongoDBUri` mit Ihren eigenen Werten.

### Starten der Anwendung

Führen Sie die Anwendung mit Flask aus:
```bash
flask run
```

Öffnen Sie einen Webbrowser und navigieren Sie zu `http://127.0.0.1:5000/`, um die Anwendung zu verwenden.

## Konfiguration

- `SECRET_KEY`: Ein geheimer Schlüssel, der für die sichere Speicherung von Session-Daten verwendet wird.
- `MONGO_URI`: Die URI Ihrer MongoDB-Instanz, die verwendet wird, um eine Verbindung zur Datenbank herzustellen.
- `UPLOADED_PHOTOS_DEST`: Der Pfad, unter dem hochgeladene Fotos gespeichert werden.

## Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe die [LICENSE.md](LICENSE.md) Datei für Details.
