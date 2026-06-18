# 🚀 Lancer le projet

Guide de démarrage du **Wedding Invitation SaaS** en local. Vue d'ensemble du projet : [README.md](README.md).

---

## 1. Prérequis

- [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) installé **et démarré**
- [**mkcert**](https://github.com/FiloSottile/mkcert) (certificats HTTPS locaux) — `brew install mkcert nss` sur macOS
- Git

---

## 2. Certificats HTTPS (à faire une fois)

Le backend et le frontend sont servis en **HTTPS**. Il faut générer des certificats locaux approuvés avec mkcert et les placer dans `backend/certs/` **et** `frontend/certs/`.

```bash
# Installe l'autorité de certification locale dans le trousseau système (une fois)
mkcert -install

# Génère le certificat pour localhost dans les deux dossiers
mkdir -p backend/certs frontend/certs
mkcert -key-file backend/certs/localhost-key.pem  -cert-file backend/certs/localhost.pem  localhost 127.0.0.1
mkcert -key-file frontend/certs/localhost-key.pem -cert-file frontend/certs/localhost.pem localhost 127.0.0.1
```

> Ces dossiers `certs/` sont **gitignorés** : chaque développeur génère les siens.
> Sans certificats, Vite et Uvicorn retombent en HTTP — mais les variables d'URL attendent `https://` (voir plus bas).

---

## 3. Fichiers d'environnement

Copier l'exemple côté frontend :

```bash
cp frontend/.env.example frontend/.env
```

Renseigner les clés **Firebase** (login Google) dans `frontend/.env`. `VITE_API_URL` y est déjà fixé à `https://localhost:8000`.

Pour **Stripe** (paiement, optionnel), créer un `.env` à la racine :

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
# Optionnel — ont déjà des défauts de dev dans docker-compose :
# SECRET_KEY=...           (⚠️ à changer pour la prod)
# FRONTEND_URL=https://localhost:5173
# BACKEND_URL=https://localhost:8000
```

---

## 4. Démarrage

```bash
# Build + lance les 4 services en arrière-plan
docker compose up -d --build

# Vérifie que tout tourne (4 services "Up")
docker compose ps
```

Tu dois voir : `wedding_db`, `wedding_api`, `wedding_ui`, `wedding_adminer`.

---

## 5. Seeder la base (à faire une fois)

Comptes de test + galerie de templates :

```bash
docker exec wedding_api python scripts/seed_all.py
```

> Les templates sont aussi ré-activés automatiquement à chaque démarrage du backend (`seed_data()` dans `main.py`). Le seed manuel sert surtout aux **comptes de démo**.

---

## 6. Ouvrir l'application

| Service             | URL                            |
|---------------------|--------------------------------|
| **Application**     | https://localhost:5173         |
| Docs API (Swagger)  | https://localhost:8000/docs    |
| Adminer (BDD)       | http://localhost:8080          |

Comptes de test (mot de passe `password123`) : `marie@classic.com`, `thomas@premium.com`, `admin@wedding.com`.

> À la première visite, le navigateur peut demander d'accepter le certificat de `https://localhost:8000` — visite l'URL une fois et accepte, sinon les appels API échouent silencieusement.

---

## Commandes utiles

```bash
docker compose logs -f backend     # logs API en direct
docker compose logs -f frontend    # logs Vite
docker compose restart backend     # recharger le backend (après modif Python / .env)
docker compose exec backend bash   # shell dans le conteneur API
docker compose down                # stop (conserve les données)
docker compose down -v             # stop + RESET complet de la BDD
```

> Le code (`backend/` et `frontend/`) est **monté en volume** : les modifications sont rechargées à chaud (Uvicorn `--reload`, Vite HMR). Seuls les changements de `docker-compose.yaml` ou de variables d'env nécessitent `docker compose up -d` (recréation du conteneur).

---

## Tests backend

Base SQLite en mémoire — aucune dépendance à Docker :

```bash
cd backend
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/ -v
```

---

## Résolution des problèmes

| Problème | Cause / Solution |
|----------|------------------|
| `ERR_EMPTY_RESPONSE` sur l'API, login/upload/paiement « ne marche pas » | Le front appelle l'API en `http://` alors qu'elle est en **HTTPS**. Vérifier `VITE_API_URL=https://localhost:8000`, `BACKEND_URL` et `FRONTEND_URL` en `https`. |
| Appels API qui échouent sans erreur claire | Certificat de `https://localhost:8000` non approuvé. Lancer `mkcert -install` puis visiter l'URL une fois. |
| Galerie de templates vide | `docker exec wedding_api python scripts/seed_all.py` |
| Port 5432 déjà utilisé | Un PostgreSQL local tourne : `brew services stop postgresql` |
| Login **Google** plante dans Safari | Limitation navigateur (ITP) en local. Utiliser **Chrome** en dev ; en prod, mettre `authDomain` sur un domaine perso. Le login **email/mot de passe** marche partout. |
| `MODULE_NOT_FOUND` au build | `docker compose down -v && docker compose up -d --build` |
