# Backend — Documentation Technique

API REST construite avec **FastAPI** et **PostgreSQL**. Gère l'authentification, les événements, les cartes d'invitation, les invités, le plan de table et les paiements.

---

## Stack

| Outil              | Version  | Rôle                             |
|--------------------|----------|----------------------------------|
| Python             | 3.10     |                                  |
| FastAPI            | 0.125    | Framework web async              |
| SQLAlchemy         | 2.0      | ORM                              |
| PostgreSQL         | 15       | Base de données principale       |
| Pydantic v2        | 2.12     | Validation des données / schemas |
| python-jose        | —        | Génération et vérification JWT   |
| passlib + bcrypt   | —        | Hashage des mots de passe        |
| firebase-admin     | —        | Vérification des tokens Google   |
| stripe             | —        | Paiement                         |
| boto3              | —        | Stockage S3 (images/musique)     |
| Pillow             | —        | Traitement d'images              |

---

## Structure

```
backend/
├── app/
│   ├── main.py                  Point d'entrée FastAPI + seed au démarrage
│   ├── api/
│   │   ├── deps.py              Dépendances (auth, session DB)
│   │   ├── plans.py             Limites par plan (classic / premium)
│   │   └── api_v1/
│   │       ├── api.py           Enregistrement de tous les routers
│   │       └── endpoints/
│   │           ├── auth.py      Login, signup, Google OAuth, refresh token
│   │           ├── cards.py     CRUD cartes + upload media
│   │           ├── events.py    CRUD événements
│   │           ├── guests.py    CRUD invités + RSVP
│   │           ├── payments.py  Webhooks Stripe + upgrade plan
│   │           ├── table.py     Plan de table
│   │           ├── templates.py Liste des templates
│   │           └── users.py     Profil utilisateur + admin
│   ├── core/
│   │   ├── config.py            Paramètres via pydantic-settings (.env)
│   │   ├── security.py          JWT (access + refresh token)
│   │   └── storage.py           Upload S3 + URLs signées
│   ├── db/
│   │   └── session.py           Connexion SQLAlchemy + SessionLocal
│   ├── models/
│   │   └── wedding.py           Tous les modèles ORM
│   ├── schemas/
│   │   ├── card.py              Schemas Pydantic carte / template / RSVP
│   │   ├── event.py             Schemas événement
│   │   ├── guest.py             Schemas invité
│   │   ├── table.py             Schemas table
│   │   ├── token.py             Schemas token JWT
│   │   └── user.py              Schemas utilisateur
│   └── tests/
│       ├── conftest.py          Fixtures pytest (DB SQLite en mémoire)
│       ├── test_auth.py
│       ├── test_cards.py
│       ├── test_events.py
│       ├── test_guests.py
│       └── test_tables.py
└── scripts/
    ├── seed_all.py              Lance tous les seeds (à exécuter après install)
    └── seed_users.py            Crée les comptes de test
```

---

## Modèles de données

```
User ──< Event ──< Card ──< SubEvent
                       └──< CardVersion
         │
         └──< Guest ──< RSVP
         │
         └──< WeddingTable >──< Guest  (many-to-many via guest_table)

CardTemplate  (catalogue global des templates, indépendant des users)
```

### Modèles principaux

**User** — compte utilisateur  
- `plan` : `classic` ou `premium`  
- `is_admin` : accès admin

**Event** — mariage  
- Appartient à un `User`  
- Contient `groom_name`, `bride_name`, `date`, `location`  
- Possède une seule `Card` et plusieurs `Guest`

**Card** — l'invitation digitale  
- Liée à un `Event` (1-to-1)  
- `template_id` : référence le template choisi  
- `config_json` : configuration complète de l'invitation (layout, thème, contenu, sections)  
- `slug` : identifiant URL public (`/cards/:slug`)  
- `is_published` : contrôle la visibilité publique

**CardTemplate** — template du catalogue  
- `id` : clé slug (ex : `noir-eternel`, `gatsby`)  
- `manifest_json` : config JSON par défaut du template  
- `category` : `minimal`, `classic`, `art`, `boho`  
- `is_active` : activé automatiquement au démarrage

**Guest** — invité  
- `rsvp_status` : `pending`, `confirmed`, `declined`  
- `plus_ones` : nombre d'accompagnants  
- `parent_id` : auto-référence (invités secondaires rattachés à un invité principal)

---

## Authentification

Deux méthodes supportées :

**Email / mot de passe** — `POST /auth/login` (OAuth2 password flow)  
**Google OAuth** — `POST /auth/google` (token Firebase → vérification côté serveur → JWT interne)

Tokens :
- **Access token** : durée 24h (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Refresh token** : durée 7 jours, renouvelable via `POST /auth/refresh-token`

Tous les endpoints protégés reçoivent le token en header `Authorization: Bearer <token>`.

---

## Templates — mécanisme de catalogue

`TEMPLATE_CATALOG` dans `main.py` est la source de vérité unique pour les 16 templates actifs.

Au démarrage (`seed_data()`) :
1. La colonne `category` est créée si elle n'existe pas encore (migration safe)
2. Chaque template du catalogue est activé + mis à jour (thumbnail, catégorie, nom)
3. Tout template absent du catalogue est désactivé

Ce système est **idempotent** : il tourne à chaque `docker-compose up` sans effet de bord.

---

## Plans et limites

Définis dans `app/api/plans.py` :

| Limite           | classic | premium |
|------------------|---------|---------|
| Invités max      | 50      | illimité |
| Photos galerie   | 5       | illimité |
| Templates accès  | tous    | tous    |

---

## Routes API

| Méthode | Route                        | Description                           |
|---------|------------------------------|---------------------------------------|
| POST    | `/auth/signup`               | Créer un compte                       |
| POST    | `/auth/login`                | Connexion email/mot de passe          |
| POST    | `/auth/google`               | Connexion Google                      |
| POST    | `/auth/refresh-token`        | Renouveler le token                   |
| GET     | `/auth/me`                   | Profil de l'utilisateur connecté      |
| GET     | `/events/`                   | Lister ses événements                 |
| POST    | `/events/`                   | Créer un événement                    |
| GET     | `/events/:id`                | Détail d'un événement                 |
| PUT     | `/events/:id`                | Modifier un événement                 |
| GET     | `/cards/`                    | Lister ses cartes                     |
| GET     | `/cards/:id`                 | Détail d'une carte                    |
| PUT     | `/cards/:id/save`            | Sauvegarder config + template         |
| POST    | `/cards/:id/upload-media`    | Upload photo/musique                  |
| GET     | `/cards/public/:slug`        | Carte publique (sans auth)            |
| GET     | `/templates/`                | Lister les templates actifs           |
| GET     | `/guests/event/:id`          | Invités d'un événement                |
| POST    | `/guests/`                   | Ajouter un invité                     |
| PUT     | `/guests/:id`                | Modifier un invité                    |
| DELETE  | `/guests/:id`                | Supprimer un invité                   |
| POST    | `/guests/:id/rsvp`           | Soumettre un RSVP (public)            |
| GET     | `/tables/event/:id`          | Tables d'un événement                 |
| POST    | `/tables/`                   | Créer une table                       |
| POST    | `/payments/create-checkout`  | Créer une session Stripe              |
| POST    | `/payments/webhook`          | Webhook Stripe (mise à jour du plan)  |

Documentation interactive complète : **http://localhost:8000/docs**

---

## Variables d'environnement

| Variable                      | Obligatoire | Défaut   | Description                    |
|-------------------------------|-------------|----------|--------------------------------|
| `DATABASE_URL`                | Oui         | —        | URL PostgreSQL                 |
| `SECRET_KEY`                  | Oui         | `mdp123` | Clé de signature JWT           |
| `ALGORITHM`                   | Non         | `HS256`  | Algorithme JWT                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Non         | `1440`   | Durée access token (minutes)   |
| `STRIPE_SECRET_KEY`           | Non         | —        | Clé Stripe (paiement)          |
| `STRIPE_WEBHOOK_SECRET`       | Non         | —        | Secret webhook Stripe          |
| `S3_BUCKET`                   | Non         | —        | Bucket S3 (uploads)            |
| `S3_ACCESS_KEY`               | Non         | —        | Clé AWS                        |
| `S3_SECRET_KEY`               | Non         | —        | Secret AWS                     |

---

## Lancer les tests

```bash
cd backend
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/ -v
```

Les tests utilisent une base SQLite en mémoire — aucune dépendance à PostgreSQL ou Docker.
