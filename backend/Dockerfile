# Utilise une image Python légère
FROM python:3.10-slim

# Définit le dossier de travail dans le container
WORKDIR /app

# Copie le fichier de dépendances
COPY requirements.txt .

# Installe les outils listés dans ton requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste du code du dossier backend
COPY . .

# Lance le serveur FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

