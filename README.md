# WeddingInvitationSaaS 💍

MariageManager est une plateforme SaaS permettant de créer et gérer des invitations de mariage numériques. Elle inclut une gestion des invités, des RSVP et des plans de table.

---

## 🚀 Lancement rapide

### 1️⃣ Prérequis
Assurez-vous d'avoir installé :
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Node.js](https://nodejs.org/) (version 18+)

### 2️⃣ Installation & Lancement du Backend (Docker)
Le backend utilise FastAPI, PostgreSQL et Adminer pour la gestion de la base de données.

```bash
# Lancer les services (Base de données, API, Adminer)
docker compose up -d --build
```

*Note : Le premier lancement peut prendre quelques minutes pour construire l'image Python.*

### 3️⃣ Lancement du Frontend (Vue.js)
Dans un nouveau terminal :

```bash
cd frontend
npm install
npm run dev
```

---

## 🛠 Accès aux services

| Service | URL | Identifiants / Notes |
| :--- | :--- | :--- |
| **Frontend** | [http://localhost:5173](http://localhost:5173) | Interface Vue 3 |
| **API Swagger** | [http://localhost:8000/docs](http://localhost:8000/docs) | Pour tester les endpoints (Auth, etc.) |
| **Adminer (BDD)** | [http://localhost:8080](http://localhost:8080) | Voir ci-dessous pour la connexion |

### 🔑 Connexion à la Base de Données (Adminer)
Pour voir les données (utilisateurs, invitations...) :
- **Système :** `PostgreSQL`
- **Serveur :** `db`
- **Utilisateur :** `user`
- **Mot de passe :** `password`
- **Base de données :** `wedding_db`

---

## 📖 Structure du projet

- `/backend` : API FastAPI (Python 3.10)
  - `/app/models` : Modèles SQLAlchemy (Base de données)
  - `/app/api` : Points d'accès (Endpoints)
- `/frontend` : Application Vue.js 3 + Vite + TailwindCSS

---

## 🆘 Dépannage
- **Port 8000 déjà utilisé** : Si vous avez un autre serveur lancé sur le port 8000, le backend Docker ne pourra pas démarrer. Arrêtez le processus local ou changez le port dans `docker-compose.yaml`.
- **Erreur de connexion BDD** : Si l'API affiche une erreur de connexion au premier lancement, redémarrez le conteneur backend : `docker compose restart backend`.
