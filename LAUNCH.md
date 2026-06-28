# Lancer le projet

---

## Démarrage rapide

```bash
# 1. Certificats HTTPS (une seule fois par machine)
mkcert -install
mkdir -p backend/certs frontend/certs
mkcert -key-file backend/certs/localhost-key.pem  -cert-file backend/certs/localhost.pem  localhost 127.0.0.1
mkcert -key-file frontend/certs/localhost-key.pem -cert-file frontend/certs/localhost.pem localhost 127.0.0.1

# 2. Variables d'environnement (une seule fois)
cp frontend/.env.example frontend/.env
# → renseigner les clés Firebase dans frontend/.env

# 3. Lancer tous les services
docker compose up -d --build

# 4. Vérifier que les 4 services tournent
docker compose ps
```
## Tests backend

```bash
docker compose exec backend bash -c "DATABASE_URL='sqlite:///./test.db' python -m pytest app/tests/ -v"
```

## Bdd

```bash
docker exec wedding_db psql -U user -d wedding_db -c "SELECT id, email, plan, is_admin FROM users;"
```


---

## Accès à l'application

| Service | URL |
|---|---|
| **Application** | https://localhost:5173 |
| **Docs API (Swagger)** | https://localhost:8000/docs |
| **Adminer (BDD)** | http://localhost:8080 |

> A la première visite, accepter le certificat de `https://localhost:8000` dans le navigateur, sinon les appels API échouent.

---

## Comptes de test

Mot de passe de tous les comptes : **`password123`**

| Email | Forfait | Admin |
|---|---|---|
| `marie@classic.com` | classic | Non |
| `thomas@premium.com` | premium | Non |
| `admin@wedding.com` | premium | Oui |

---

## Accès à la base de données

### Adminer — http://localhost:8080

| Champ | Valeur |
|---|---|
| Système | `PostgreSQL` |
| Serveur | `db` |
| Utilisateur | `user` |
| Mot de passe | `password` |
| Base | `wedding_db` |

> Le serveur est `db` (nom interne Docker), pas `localhost`.

### psql en ligne de commande

```bash
# Shell interactif
docker exec -it wedding_db psql -U user -d wedding_db

# Lister les comptes
docker exec wedding_db psql -U user -d wedding_db -c "SELECT id, email, plan, is_admin FROM users;"

# Passer un compte en admin
docker exec wedding_db psql -U user -d wedding_db -c "UPDATE users SET is_admin = true WHERE email = 'moi@test.com';"

# Passer un compte en premium
docker exec wedding_db psql -U user -d wedding_db -c "UPDATE users SET plan = 'premium' WHERE email = 'moi@test.com';"
```

---



## Commandes utiles

```bash
docker compose logs -f backend     # logs API en direct
docker compose logs -f frontend    # logs Vite
docker compose restart backend     # relancer le backend (après modif Python / .env)
docker compose exec backend bash   # shell dans le conteneur API
docker compose down                # stopper (conserve les données)
docker compose down -v             # stopper + reset complet de la BDD
```

---

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré
- [mkcert](https://github.com/FiloSottile/mkcert) — `brew install mkcert nss` sur macOS
- Git

---

## Variables d'environnement Stripe (optionnel)

Créer un `.env` à la racine du projet :

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Résolution des problèmes

| Problème | Solution |
|---|---|
| Login/upload/paiement ne marche pas | Vérifier `VITE_API_URL=https://localhost:8000` dans `frontend/.env` |
| Appels API échouent sans erreur | Accepter le certificat en visitant `https://localhost:8000` une fois |
| Galerie de templates vide | `docker exec wedding_api python scripts/seed_all.py` |
| Port 5432 déjà utilisé | `brew services stop postgresql` |
| Login Google plante dans Safari | Utiliser Chrome en local |
| `MODULE_NOT_FOUND` au build | `docker compose down -v && docker compose up -d --build` |
| Base corrompue / repartir à zéro | `docker compose down -v && docker compose up -d` |
