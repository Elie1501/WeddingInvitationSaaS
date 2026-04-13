# Saas Wedding 💍

Saas Wedding est une plateforme SaaS permettant de créer et gérer des invitations de mariage numériques. Elle inclut une gestion des invités, des RSVP et des plans de table.

---

## 🚀 Installation & Lancement rapide

### 🐳 Option A : Via Docker (Recommandé)

Docker compose s'occupe de tout : Base de données, API, Adminer et Frontend.

```bash
# Lancer tous les services
docker compose up -d --build
```

- **Frontend** : [http://localhost:5173](http://localhost:5173)
- **API Swagger** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Adminer (BDD)** : [http://localhost:8080](http://localhost:8080)

---

### 🐍 Option B : Lancement Manuel (Sans Docker)

#### 🛠 Pré-requis
- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **libmagic** (Analyse de fichiers) :
  - macOS : `brew install libmagic`
  - Linux : `sudo apt-get install libmagic1`

#### 1. Base de données (PostgreSQL)
1. Créez la BDD : `createdb wedding_db`
2. Configurez `backend/.env` : `DATABASE_URL=postgresql:///wedding_db`

#### 2. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Init BDD & Test Users
python -m scripts.reset_db_schema
python -m scripts.seed_users

uvicorn app.main:app --reload --port 8000
```

#### 3. Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev -- --port 5173
```

---

## 🔑 Identifiants & Comptes de test

### 👤 Comptes Utilisateurs
Tous les comptes utilisent le mot de passe : **`password123`**

| Email | Plan | Rôle suggéré |
| :--- | :--- | :--- |
| `admin@wedding.com` | `premium` | Administrateur / Test Complet |
| `test@test.com` | `premium` | Compte de test rapide |
| `marie@classic.com` | `classic` | Test plan classique |
| `thomas@premium.com` | `premium` | Test plan premium |

### 🗄️ Base de données (PostgreSQL)
- **Adminer** : [http://localhost:8080](http://localhost:8080)
- **Host** : `db` (Docker) ou `localhost` (Manuel)
- **User** : `user` (Docker) ou votre utilisateur OS (Manuel)
- **Password** : `password` (Docker) ou vide (Manuel par défaut)
- **DB** : `wedding_db`

---

## ⚙️ Configuration (.env)

Le fichier `.env` se trouve dans `backend/`.

| Variable | Description | Exemple |
| :--- | :--- | :--- |
| `DATABASE_URL` | Connexion BDD | `postgresql:///wedding_db` |
| `SECRET_KEY` | Clé JWT | `votre_cle_secrete` |
| `S3_BUCKET` | Bucket Media | `wedding-invitations-media` |

*Note : Si S3 n'est pas configuré, les fichiers sont stockés dans `backend/uploads/`.*

---

## 🧪 Scripts de maintenance (Dossier backend)

```bash
# Réinitialiser complètement la BDD (Tables + Data)
python -m scripts.reset_db_schema
# Ajouter/Restaurer les utilisateurs de test
python -m scripts.seed_users
# Forcer la création du compte test@test.com
python -m scripts.force_seed
```

---

## 🛠 Guide d'utilisation de l'API (Swagger UI)

1.  **URL** : [http://localhost:8000/docs](http://localhost:8000/docs)
2.  **S'authentifier** : `POST /auth/login` avec vos identifiants.
3.  **Authorize** : Cliquez sur le bouton "Authorize" en haut à droite et entrez vos accès.
