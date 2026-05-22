import requests
import json

# ==============================================================================
# ZF API Chatbot - Client Beispiel
# ==============================================================================

API_URL = "http://<SERVER-IP>:8000/chat"

def ask_chatbot(prompt, model="deepseek-r1:8b"):
    """
    Sendet eine Anfrage an das ZF API Chatbot Gateway.
    """
    payload = {
        "prompt": prompt,
        "model": model
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Sende Anfrage an Chatbot ({model})...")
        response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        
        # Prüfen, ob der Server einen Fehler gemeldet hat
        response.raise_for_status()
        
        # Antwort parsen
        data = response.json()
        return data["response"]

    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    # Test-Anfrage
    frage = "Erkläre kurz, was ein API-Gateway ist."
    antwort = ask_chatbot(frage)
    
    print("\n--- Antwort vom ZF API Chatbot ---")
    print(antwort)
    print("----------------------------------\n")
