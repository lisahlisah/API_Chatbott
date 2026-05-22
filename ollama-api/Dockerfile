# Basis-Image: schlankes Python 3.11
FROM python:3.11-slim   

# Arbeitsverzeichnis im Container
WORKDIR /app

# Zuerst nur requirements kopieren (Docker-Cache-Trick, siehe unten)
COPY requirements.txt .

# Pakete installieren
RUN pip install --no-cache-dir -r requirements.txt

# Dann den restlichen Code kopieren
COPY ./app ./app

# Port nach außen freigeben
EXPOSE 8000

# Startbefehl wenn der Container hochfährt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]