# Backend — Documentation technique

API REST en **FastAPI** + **PostgreSQL**. Gère l'authentification, les événements, les cartes d'invitation, les invités, le plan de table, les templates et les paiements Stripe.

> Vue d'ensemble du projet : [../README.md](../README.md) · Démarrage : [../LAUNCH.md](../LAUNCH.md)

---

## Stack

| Outil            | Version | Rôle                                  |
|------------------|---------|---------------------------------------|
| Python           | 3.10    | Runtime                               |
| FastAPI          | 0.125   | Framework web                         |
| Uvicorn          | 0.38    | Serveur ASGI (lancé en **HTTPS/SSL**) |
| SQLAlchemy       | 2.0     | ORM                                   |
| PostgreSQL       | 15      | Base de données                       |
| Pydantic v2      | 2.12    | Validation / schémas / settings       |
| python-jose      | —       | JWT (signature/vérification)          |
| passlib + bcrypt | —       | Hash des mots de passe                |
| firebase-admin   | —       | Vérification des tokens Google        |
| stripe           | —       | Paiement                              |
| boto3            | —       | Stockage S3 (repli local sinon)       |
| Pillow           | —       | Optimisation d'images à l'upload      |
| python-magic     | —       | Détection du type MIME des uploads    |

Dépendances exactes : [`requirements.txt`](requirements.txt).

---

## Structure

```
backend/
├── Dockerfile                  Image Python + uvicorn (SSL)
├── requirements.txt            Dépendances runtime
├── certs/                      Certificats mkcert (gitignorés)
└── app/
    ├── main.py                 Point d'entrée FastAPI, CORS, mount /uploads, seed_data() au démarrage
    ├── api/
    │   ├── deps.py             Dépendances : get_current_user (+ is_active), check_plan_permission, require_paid_plan, require_premium, require_admin
    │   ├── plans.py            PLAN_PRICES, PLAN_LIMITS (max_sites/pages, can_upload_music, can_export_csv, can_custom_slug, can_edit_typography…), NONE_LIMITS, PREMIUM_SECTION_IDS, get_limits()
    │   └── api_v1/
    │       ├── api.py          Agrège tous les routers (préfixes /auth, /events, …)
    │       └── endpoints/
    │           ├── auth.py     signup, login, google, refresh-token, me
    │           ├── users.py    profil + endpoints admin (liste, stats, statut, suppression)
    │           ├── events.py   CRUD événements + carte publique par slug
    │           ├── cards.py    CRUD cartes, save, publish, upload média, import/export, versions
    │           ├── guests.py   CRUD invités + RSVP public
    │           ├── table.py    plan de table (CRUD, assign/unassign, export CSV)
    │           ├── templates.py liste des templates actifs
    │           └── payments.py checkout, upgrade, confirm-payment, webhook Stripe
    ├── core/
    │   ├── config.py           Settings via pydantic-settings (.env) — URLs, secrets, Stripe, S3
    │   ├── security.py         Création/validation JWT (access + refresh), hash mots de passe
    │   ├── csv_utils.py        csv_safe() — anti-injection de formules dans les exports CSV
    │   ├── ratelimit.py        rate_limit() — limiteur en mémoire par IP (login, RSVP public)
    │   └── storage.py          Upload S3 OU local (/uploads) + génération d'URL
    ├── db/
    │   └── session.py          Engine SQLAlchemy + SessionLocal + get_db()
    ├── models/
    │   └── wedding.py          Tous les modèles ORM (tables)
    ├── schemas/                Schémas Pydantic (entrées/sorties d'API)
    │   ├── card.py  event.py  guest.py  table.py  token.py  user.py
    └── tests/                  Pytest (SQLite en mémoire) — auth, cards, events, guests, tables, payments, admin
```

`scripts/` contient les seeds (`seed_all.py`, `seed_users.py`, seeds de templates…).

---

## Modèle de données (`models/wedding.py`)

```
User ──< Event ──1:1── Card ──< SubEvent      (programme)
  │         │             └──< CardVersion     (historique éditeur)
  │         ├──< Guest ──< RSVP
  │         └──< WeddingTable >──< Guest        (N:N, table guest_table)
CardTemplate                                    (catalogue global)
```

| Modèle         | Colonnes clés                                                                 |
|----------------|-------------------------------------------------------------------------------|
| `User`         | `email`, `hashed_password`, `plan` (`classic`/`premium`), `is_admin`, `is_active` |
| `Event`        | `title`, `groom_name`, `bride_name`, `date`, `location`, `owner_id`           |
| `Card`         | `event_id` (unique), `template_id`, `slug` (unique), `config_json`, `is_published`, `has_cover_page`, `media_url`, `music_url` |
| `CardTemplate` | `id` (slug), `name`, `manifest_json`, `thumbnail_url`, `category`, `required_plan`, `is_active` |
| `SubEvent`     | `card_id`, `title`, `time`                                                     |
| `CardVersion`  | snapshot d'une version d'éditeur                                              |
| `Guest`        | `event_id`, `first_name`, `last_name`, `rsvp_status`, `parent_id`, `dietary_restrictions`, `message` |
| `RSVP`         | trace de réponse (`presence`, `plus_ones`)                                    |
| `WeddingTable` | `event_id`, `name`, `capacity` + relation N:N vers `Guest`                     |

---

## Authentification

Deux méthodes :

- **Email / mot de passe** — `POST /auth/signup` puis `POST /auth/login` (OAuth2 password flow, mot de passe haché bcrypt).
- **Google** — `POST /auth/google` : le front envoie un `id_token` Firebase, le backend le **vérifie** (firebase-admin) puis émet ses propres JWT.

Tokens (`core/security.py`) :
- **Access token** — 24 h (`ACCESS_TOKEN_EXPIRE_MINUTES`), envoyé en header `Authorization: Bearer <token>`.
- **Refresh token** — 7 jours, renouvelé via `POST /auth/refresh-token`.

`deps.get_current_user` décode le JWT, charge l'utilisateur et **rejette les comptes désactivés** (`is_active = false`).

---

## Sécurité (modèle d'autorisation)

> Les gardes du frontend sont contournables — **toute l'autorisation est ré-imposée ici.**

- **Anti-IDOR** : chaque endpoint sur une carte/événement/invité/table filtre sur `Event.owner_id == current_user.id`. On ne peut pas accéder aux données d'un autre user via l'ID dans l'URL.
- **Admin** : les routes `/users/*` d'administration passent par la dépendance **`require_admin`** (403 sinon) — contrôle centralisé, plus de check `is_admin` recopié à la main dans chaque endpoint. Un admin ne peut pas se supprimer lui-même (400).
- **Paywall** : la création d'événement exige `require_paid_plan` (402 tant qu'aucun forfait payé).
- **Règle métier (tables)** : un invité ne peut être affecté qu'à une table **du même événement** (`table.event_id == guest.event_id`, 400 sinon), en plus du contrôle de capacité.
- **Gating forfait** : `check_plan_permission(...)` (export CSV, URL personnalisée, tables), `_enforce_plan_features(...)` (blocs premium à la sauvegarde), limites de pages/sites, templates `required_plan`. `get_limits("none")` renvoie **un jeu tout verrouillé** (paywall défensif — pas de repli sur Classic).
- **Upload** (`/cards/{id}/upload`) : type **et** extension validés (allowlist), **SVG/HTML refusés** (XSS stocké via `/uploads`), lecture **en flux plafonnée** (image ≤ 10 Mo, audio ≤ 20 Mo → 413/415 sinon).
- **CORS** (`main.py`) : liste d'origines explicites (`FRONTEND_URL` + dev) — jamais `*` avec `allow_credentials`.
- **Exports CSV** (`core/csv_utils.py`) : neutralisation de l'**injection de formules** (préfixe `'` sur les valeurs commençant par `= + - @`).
- **Rate-limiting** (`core/ratelimit.py`, en mémoire/IP) : `login` (10/5 min, anti brute-force) et `public/rsvp` (15/5 min, anti-spam). Le RSVP public ne cible que les invités principaux et n'écrase pas un homonyme ayant un autre email.
- **Paiement** : `plan` n'est modifié que par `confirm-payment` (session Stripe `paid` + `user_id` du token) ou le `webhook` signé. Garde anti double-paiement dans `create-checkout-session`, anti re-upgrade dans `create-upgrade-session`.

---

## Routes API

Base : `https://localhost:8000`. Documentation interactive : **`/docs`**. (🔒 = auth requise, 👑 = admin, ⭐ = premium, 🌐 = public.)

### `/auth`
| Méthode | Route                  | Accès | Description                          |
|---------|------------------------|:-----:|--------------------------------------|
| POST    | `/auth/signup`         | 🌐    | Créer un compte                      |
| POST    | `/auth/login`          | 🌐    | Connexion email/mot de passe         |
| POST    | `/auth/google`         | 🌐    | Connexion Google (id_token Firebase) |
| POST    | `/auth/refresh-token`  | 🌐    | Renouveler l'access token            |
| GET     | `/auth/me`             | 🔒    | Profil courant                       |

### `/events`
| Méthode | Route                          | Accès | Description                         |
|---------|--------------------------------|:-----:|-------------------------------------|
| GET     | `/events/`                     | 🔒    | Lister ses événements               |
| POST    | `/events/`                     | 🔒    | Créer un événement (vérifie limite) |
| GET     | `/events/{id}`                 | 🔒    | Détail (ownership)                  |
| PUT     | `/events/{id}`                 | 🔒    | Modifier                            |
| DELETE  | `/events/{id}`                 | 🔒    | Supprimer                           |
| POST    | `/events/admin/sync-cards-data`| 🔒    | Resync nom/date/lieu dans la config (ses cartes uniquement) |
| GET     | `/events/public/card/{slug}`   | 🌐    | Carte publique par slug (DTO filtré) |

### `/cards`
| Méthode | Route                        | Accès | Description                          |
|---------|------------------------------|:-----:|--------------------------------------|
| GET     | `/cards/`                    | 🔒    | Lister ses cartes                    |
| POST    | `/cards/`                    | 🔒    | Créer une carte pour un événement    |
| GET     | `/cards/{id}`                | 🔒    | Détail                               |
| PUT     | `/cards/{id}/save`           | 🔒    | Auto-save config (gating premium)    |
| POST    | `/cards/{id}/publish`        | 🔒    | Publier / dépublier (génère le slug) |
| PATCH   | `/cards/{id}/slug`           | 🔒 ⭐ | URL personnalisée (slugify + unicité) |
| POST    | `/cards/{id}/upload`         | 🔒    | Upload image / musique — type + taille validés (musique : **tous forfaits**) |
| GET     | `/cards/{id}/export`         | 🔒    | Export JSON de la carte              |
| POST    | `/cards/{id}/import`         | 🔒    | Import JSON (⭐)                       |
| GET     | `/cards/{id}/versions`       | 🔒    | Historique                           |
| POST    | `/cards/{id}/rollback/{n}`   | 🔒    | Restaurer une version                |
| DELETE  | `/cards/{id}`                | 🔒    | Supprimer                            |

### `/guests`
| Méthode | Route                        | Accès | Description                       |
|---------|------------------------------|:-----:|-----------------------------------|
| GET     | `/guests/event/{event_id}`   | 🔒    | Invités d'un événement            |
| POST    | `/guests/`                   | 🔒    | Ajouter un invité                 |
| PATCH   | `/guests/{id}`               | 🔒    | Modifier                          |
| DELETE  | `/guests/{id}`               | 🔒    | Supprimer                         |
| GET     | `/guests/event/{id}/rsvps`   | 🔒    | Réponses RSVP                     |
| GET     | `/guests/event/{id}/export/csv` | 🔒 ⭐ | Export CSV des invités          |
| POST    | `/guests/public/rsvp`        | 🌐    | Réponse RSVP d'un invité (rate-limité) |

### `/tables`
| Méthode | Route                                 | Accès | Description              |
|---------|---------------------------------------|:-----:|--------------------------|
| GET     | `/tables/event/{event_id}`            | 🔒    | Tables d'un événement    |
| POST    | `/tables/`                            | 🔒    | Créer une table          |
| PUT     | `/tables/{id}`                        | 🔒    | Modifier                 |
| DELETE  | `/tables/{id}`                        | 🔒    | Supprimer                |
| POST    | `/tables/{id}/assign/{guest_id}`      | 🔒    | Asseoir un invité (même événement + capacité) |
| POST    | `/tables/{id}/unassign/{guest_id}`    | 🔒    | Retirer un invité        |
| GET     | `/tables/event/{id}/export/csv`       | 🔒 ⭐ | Export CSV du plan       |

### `/templates` · `/payments`
| Méthode | Route                                | Accès | Description                       |
|---------|--------------------------------------|:-----:|-----------------------------------|
| GET     | `/templates/`                        | 🌐    | Templates actifs du catalogue     |
| POST    | `/payments/create-checkout-session`  | 🔒    | Achat plein tarif (garde anti double-paiement) |
| POST    | `/payments/create-upgrade-session`   | 🔒    | Upgrade Classic→Premium (50 €)    |
| POST    | `/payments/confirm-payment`          | 🔒    | Confirme une session payée → maj plan |
| POST    | `/payments/webhook`                  | 🌐*   | Webhook Stripe signé              |

\* signature Stripe vérifiée (`STRIPE_WEBHOOK_SECRET`).

---

## Templates — catalogue

`TEMPLATE_CATALOG` dans `main.py` est la **source de vérité** des 14 templates. Au démarrage, `seed_data()` (idempotent) :
1. ajoute la colonne `category` si absente (migration douce) ;
2. active + met à jour chaque template du catalogue (thumbnail, catégorie, nom) ;
3. désactive tout template hors catalogue.

---

## Stockage des médias (`core/storage.py`)

- Si **S3 est configuré** (`S3_ACCESS_KEY`/`S3_SECRET_KEY`) → upload vers S3 + URL signée.
- Sinon → **repli local** : fichier écrit dans `uploads/`, servi par le mount statique `/uploads`. L'URL renvoyée utilise `BACKEND_URL` (**https** en dev — sinon l'image/musique ne se charge pas).
- Les images sont optimisées (redimension ≤ 1200 px, JPEG qualité 80) via Pillow.

---

## Variables d'environnement (`core/config.py`)

| Variable                      | Oblig. | Défaut                    | Rôle                                  |
|-------------------------------|:------:|---------------------------|---------------------------------------|
| `DATABASE_URL`                | Oui    | —                         | URL PostgreSQL                        |
| `SECRET_KEY`                  | Oui    | `mdp123` ⚠️               | Signature JWT (**à changer en prod**) |
| `ALGORITHM`                   | Non    | `HS256`                   | Algo JWT                              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Non    | `1440`                    | Durée access token                    |
| `FRONTEND_URL`                | Non    | `https://localhost:5173`  | Redirections retour Stripe            |
| `BACKEND_URL`                 | Non    | `https://localhost:8000`  | URLs des médias `/uploads`            |
| `STRIPE_SECRET_KEY`           | Non    | —                         | Clé Stripe                            |
| `STRIPE_WEBHOOK_SECRET`       | Non    | —                         | Secret webhook Stripe                 |
| `S3_BUCKET` / `S3_ACCESS_KEY` / `S3_SECRET_KEY` / `S3_REGION` | Non | — | Stockage S3 (sinon repli local) |

---

## Tests

**Suite : 47 tests** répartis en 8 fichiers (`app/tests/`) :

| Fichier                  | Couvre                                                        |
|--------------------------|---------------------------------------------------------------|
| `test_auth.py`           | Inscription, connexion, JWT                                   |
| `test_login_extended.py` | Cas limites de connexion / refresh                            |
| `test_cards.py`          | Création/édition/publication des cartes                       |
| `test_events.py`         | Événements + limite `max_sites` par forfait                   |
| `test_guests.py`         | Invités, RSVP, export CSV                                     |
| `test_tables.py`         | Plan de table + règle « même événement »                      |
| `test_payments.py`       | Stripe, gating premium, garde anti double-paiement            |
| `test_admin.py`          | Accès admin, blocage user/anonyme, auto-suppression interdite |

### Lancer en local (SQLite, sans Docker)

```bash
cd backend
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/ -v
```

### Reproduire la CI à l'identique (Postgres)

C'est exactement ce que joue le job **`backend-ci`** (`.github/workflows/main.yml`) — à faire tourner avant de pousser :

```bash
cd backend
export PYTHONPATH=$PYTHONPATH:.
DATABASE_URL="postgresql://user:password@localhost:5432/wedding_db" \
  SECRET_KEY=test_secret_key ALGORITHM=HS256 \
  STRIPE_SECRET_KEY=sk_test_dummy STRIPE_WEBHOOK_SECRET=whsec_dummy \
  pytest app/tests/ -v
```

### Lancer un fichier ou un test ciblé

```bash
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/test_payments.py -v          # un fichier
DATABASE_URL="sqlite:///./test.db" python -m pytest app/tests/test_payments.py::test_xxx    # un seul test
```

### Depuis un conteneur déjà lancé

```bash
docker exec wedding_api pip install -q pytest httpx
docker exec -e DATABASE_URL="sqlite:////tmp/test.db" wedding_api python -m pytest app/tests/ -v
```
