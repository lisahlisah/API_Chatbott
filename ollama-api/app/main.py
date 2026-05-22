from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx


#async = Während Ollama nachdenkt, blockiert FastAPI nicht und kann parallel Anfragen bearbeiten


#Name der API/App
app = FastAPI(title="Ollama API Gateway")

#Basis-URL des Ollama-Dienstes
OLLAMA_URL = "http://host.docker.internal:11434"

#Struktur der Daten, die der User an den /chat-Endpunkt senden muss (Request Body)
class PromptRequest(BaseModel):
    model: str = "deepseek-r1:8b"       #Das KI-Modell, kann man unter "ollama list" nachschauen
    prompt: str                         #Der Nutzer trägt die Frage oder Text ein an die KI

#Format der Daten durch das Gateway, die an den Benutzer zurückgegeben werden
class PromptResponse(BaseModel):
    model: str
    response: str



#-----------------------------------------------Endpunkt Root (/)------------------------------------------------------------#

#Statuscheck, ob die API noch lebt
@app.get("/")

#Gibt ein Python-Dictionary zurück, FastAPI konvertiert es in ein JSON-Format -> Einfacher Funktionstest für die API
def root():
    return {"status": "Ollama API Gateway läuft"}



#-----------------------------------------------Endpunkt Modelle auflisten (/models)-----------------------------------------#

#Welche Modelle hat Ollama geladen?
@app.get("/models")

#Asynchrone Funktion: Kann andere Anfragen parallel bearbeiten während Warten auf Antwort
async def list_models():
    """Zeigt alle verfügbaren Modelle in Ollama"""              #Wird in Dokumentation ausgegeben
    async with httpx.AsyncClient() as client:                   #Asynchron HTTP-Client von httpx 
        try:
            res = await client.get(f"{OLLAMA_URL}/api/tags")    #Asynchrone GET-Anfrage an /api/tags (Installierte Modelle), await wartet auf Antwort ohne Server aufzuhalten, Antwort wird in res gespeichert
            return res.json()                                   #Antwort als JSON und Übergabe an Nutzer
        except Exception:
            raise HTTPException(status_code=503, detail="Ollama nicht erreichbar")



#-----------------------------------------------Endpunkt Chat/Generierung (/chat)-------------------------------------------#

#Eigentliche Nutzung: Prompt rein, Antwort raus
@app.post("/chat", response_model=PromptResponse)

#Erwartet im Body der Anfrage Daten, die der PromptRequest entsprechen
async def chat(request: PromptRequest):
    """Schickt einen Prompt an Ollama und gibt die Antwort zurück"""
    async with httpx.AsyncClient(timeout=120.0) as client:      #Timeout da Generierung von Modell länger dauern kann als standardmäßig
        try:
            res = await client.post(                            #POST-Anfrage an /api/generate
                f"{OLLAMA_URL}/api/generate",
                json={                                      
                    "model": request.model,                     #Gewünschtes Modell
                    "prompt": request.prompt,                   #Text
                    "stream": False                             #Komplette Antwort auf einmal
                }
            )
            data = res.json()                                   #JSON-Antwort in Python-Dictionary
            return PromptResponse(model=request.model, response=data["response"])  #Gibt das Objekt zurück, Modell und Text aus response wird ausgelesen
        except httpx.TimeoutException:                          #Greift, falls 120 Sekunden überschritten sind
            raise HTTPException(status_code=504, detail="Ollama hat zu lange gebraucht")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) #500 Internal Server Error, Fehlermeldung als Text

