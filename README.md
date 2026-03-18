# MariageManager

MariageManager est un SaaS clé en main pour la **création et gestion de cartes de mariage digitales**, avec une interface simple pour les futurs mariés et une API extensible pour les développeurs.

---

## Fonctionnalités

- Création, édition et publication de cartes de mariage
- Gestion des invités et RSVP
- Organisation des tables et génération du plan de table
- Multi-forfaits : Basique, Avancé, Sur-mesure (templates personnalisés)
- Authentification sécurisée (JWT)
- API REST pour intégration et développement avancé
- Scalabilité via Docker et architecture modulaire

---

## Prérequis

- Docker & Docker Compose
- Node.js (pour le frontend)
- Git

---

## Lancement du projet

### 1️⃣ Backend et Base de données (via Docker)
Lancer les services conteneurisés (FastAPI, PostgreSQL et Adminer) :
```bash
docker compose up -d
```

### 2️⃣ Frontend (Vue.js)
Installer les dépendances et lancer le serveur de développement :
```bash
cd frontend
npm install
npm run dev
```

---

## Accès aux services

| Service | URL | Description |
| :--- | :--- | :--- |
| **Frontend** | [http://localhost:5173](http://localhost:5173) | Interface utilisateur (Vue 3 + Vite) |
| **Backend API** | [http://localhost:8000](http://localhost:8000) | API FastAPI (Documentation : [/docs](http://localhost:8000/docs)) |
| **Adminer** | [http://localhost:8080](http://localhost:8080) | Interface graphique pour la BDD |

### Connexion à Adminer :
- **Système :** `PostgreSQL`
- **Serveur :** `wedding_db`
- **Utilisateur :** `user`
- **Mot de passe :** `password`
- **Base de données :** `wedding_db`
