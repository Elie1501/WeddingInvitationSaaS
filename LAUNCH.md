# Lancer le projet

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré
- Git

---

## Démarrage rapide (tout en une commande)

```bash
docker-compose down && docker-compose up -d --build && sleep 10 && docker-compose exec backend python scripts/seed_all.py
```

Cette commande :
1. Arrête les anciens containers
2. Rebuild les images et relance tous les services
3. Attend que la base de données soit prête
4. Insère les templates et les comptes de test

---
## Démarrage étape par étape

### 1. Lancer les services

```bash
docker-compose up -d
```

Vérifie que tout tourne :

```bash
docker-compose ps
```

Tu dois voir 4 services `Up` : `wedding_db`, `wedding_api`, `wedding_ui`, `wedding_adminer`.

### 2. Seeder la base de données

À faire **une seule fois** après le premier lancement (ou après un `docker-compose down -v`) :

```bash
docker-compose exec backend python scripts/seed_all.py
```

> Les templates sont aussi auto-activés à chaque démarrage du backend via `seed_data()` dans `main.py`. Le seed manuel est surtout nécessaire pour les comptes de test.

### 3. Ouvrir l'application

- Frontend : http://localhost:5173
- Docs API (Swagger) : http://localhost:8000/docs
- Adminer (BDD) : http://localhost:8080

---

## Variables d'environnement

Les variables essentielles sont déjà définies dans `docker-compose.yaml` avec des valeurs par défaut pour le développement local.

Pour les fonctionnalités optionnelles, crée un fichier `.env` à la racine :

```env
# Stripe (paiement)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# JWT (déjà défini par défaut)
SECRET_KEY=mdp123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## Commandes utiles

```bash
# Voir les logs du backend en temps réel
docker-compose logs -f backend

# Voir les logs du frontend
docker-compose logs -f frontend

# Accéder au shell du container backend
docker-compose exec backend bash

# Relancer uniquement le backend (après une modification Python)
docker-compose restart backend

# Arrêter tous les services (conserve les données)
docker-compose down

# Arrêter ET supprimer les volumes (reset complet de la BDD)
docker-compose down -v
```

---

## Lancer les tests backend

Les tests utilisent SQLite en mémoire, pas besoin de Docker :

```bash
# macOS / Linux
cd backend
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/ -v

# Windows PowerShell
cd backend
$env:DATABASE_URL = "sqlite:///./test.db"; python -m pytest app/tests/ -v
```

---

## Résolution des problèmes courants

| Problème | Solution |
|----------|----------|
| Port 5432 déjà utilisé | Arrêter PostgreSQL local : `brew services stop postgresql` |
| Templates manquants dans la galerie | `docker-compose exec backend python scripts/seed_all.py` |
| Frontend ne se connecte pas à l'API | Vérifier que `VITE_API_URL=http://localhost:8000` dans docker-compose |
| Erreur `MODULE_NOT_FOUND` au build | `docker-compose down -v && docker-compose up -d --build` |
