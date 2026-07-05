# LabLogin
Das Projekt "LabLogin" ist eine Webanwendung auf Basis von Python und Flask, mit der sich Arbeitsplätze über vernetzte Controller (wie ESP32/ESP8266) remote einrichten und steuern lassen. Das Tool dient als Control-Panel, um vorkonfigurierte Programmlisten per HTTP-Befehl an die Controller zu senden, die dann die automatisierte Softwareinstallation oder das Starten der Umgebung auf den Zielrechnern anstoßen.
## Features
 * **Zentrales Management:** Hinzufügen und Löschen von Controllern inklusive Validierung der IP-Adressen über das Webinterface.
 * **Workspace-Konfiguration:** Zuordnung und Speicherung von spezifischen Programmlisten (z. B. VSCode, Thonny, Slicer) für einzelne Benutzer und Arbeitsplätze.
 * **API-Schnittstelle:** Automatisierter Start und Stopp der Arbeitsumgebungen über HTTP-POST-Requests inklusive Fehlerbehandlung bei Nichterreichbarkeit der Hardware.
 * **Benutzerverwaltung:** Registrierung und Login-System mit Passwort-Hashing und Session-Management.
 * **Modulare Struktur:** Saubere Aufteilung des Codes in separate Dateien für Datenbankmodelle, Routen, Konfiguration und Hilfsfunktionen.
## Installation
 1. Klonen Sie das Repository auf Ihren lokalen Computer mit dem Befehl:
```bash
git clone [https://github.com/huhncares-cmd/lab_login.git](https://github.com/huhncares-cmd/lab_login.git)

```
 2. Wechseln Sie in das Verzeichnis des geklonten Repositories:
```bash
cd lab_login

```
 3. Setzen Sie eine virtuelle Umgebung (venv) auf:
```bash
python3 -m venv venv
source venv/bin/activate

```
 4. Installieren Sie die erforderlichen Python-Pakete mit dem Befehl:
```bash
pip install -r requirements.txt

```
 5. Environment-Variablen setzen: Erstellen Sie eine .env-Datei im Stammverzeichnis mit dem Inhalt:
```env
SECRET_KEY=<dein_secret_key>
DATABASE_URL_USER=sqlite:///app.db

```
*Hinweis: Der Secret-Key kann beispielsweise über das Python-Modul secrets oder uuid generiert werden.*
## Starten
Um das Projekt zu starten, führen Sie den folgenden Befehl aus:
```bash
python run.py

```
Die Anwendung wird auf http://127.0.0.1:5000 gehostet. Die SQLite-Datenbank wird beim ersten Aufruf automatisch initialisiert.
