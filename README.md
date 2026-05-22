# ZF API Chatbot - Dokumentation

Willkommen beim ZF API Chatbot Gateway. Dieses System bietet sowohl eine grafische Benutzeroberfläche als auch eine Programmierschnittstelle (API) für Entwickler.

## 1. Zugriff auf die Weboberfläche (UI)
Öffnen Sie einfach Ihren Browser und geben Sie die Adresse des Servers ein:
`http://<SERVER-IP>:8000/`

Hier können Sie direkt im Browser mit dem Chatbot kommunizieren. Ein Lade-Indikator zeigt an, wenn der Bot nachdenkt.

## 2. API für Entwickler
Entwickler können den Chatbot direkt in ihren eigenen Anwendungen (z.B. in VSCode/Python) nutzen.

### Endpunkt: `/chat` (POST)
Senden Sie eine JSON-Anfrage an diesen Endpunkt.

**Anfrage-Struktur (JSON):**
```json
{
  "prompt": "Ihre Frage an den Bot",
  "model": "deepseek-r1:8b"
}
```

**Antwort-Struktur (JSON):**
```json
{
  "model": "deepseek-r1:8b",
  "response": "Die Antwort der KI..."
}
```

### Python Beispiel
Ein fertiges Beispiel finden Sie in der Datei `CLIENT_EXAMPLE.py`.
Voraussetzung: `pip install requests`

## 3. Interaktive API-Dokumentation (Swagger)
Eine vollständige technische Dokumentation aller Endpunkte finden Sie unter:
`http://<SERVER-IP>:8000/docs`
