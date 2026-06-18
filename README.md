# Wedding Invitation SaaS

Plateforme de création d'**invitations de mariage digitales**. Les mariés choisissent un template, personnalisent leur invitation dans un éditeur visuel, la publient sur une URL partageable, gèrent leur liste d'invités, le plan de table et suivent les réponses (RSVP) — le tout depuis une interface web.

> 📖 **Pour démarrer le projet, voir [LAUNCH.md](LAUNCH.md).**
> Docs détaillées : [backend/README.md](backend/README.md) · [frontend/README.md](frontend/README.md)

---

## Sommaire
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Fonctionnalités](#fonctionnalités)
- [Modèle de données](#modèle-de-données)
- [Forfaits (plans)](#forfaits-plans)
- [Sécurité](#sécurité)
- [HTTPS en développement local](#https-en-développement-local-important)
- [URLs & comptes de test](#urls-locales)

---

## Architecture

```
WeddingInvitationSaaS/
├── backend/            API REST — FastAPI + PostgreSQL
├── frontend/           SPA — Vue 3 + Vite + Tailwind
├── docker-compose.yaml Orchestration des 4 services
├── LAUNCH.md           Guide de démarrage pas-à-pas
└── README.md           Ce fichier (vue d'ensemble)
```

Le projet tourne entièrement via **Docker Compose**, avec 4 services :

| Service       | Conteneur         | Port  | Rôle                                   |
|---------------|-------------------|-------|----------------------------------------|
| `db`          | `wedding_db`      | 5432  | PostgreSQL 15 (données)                |
| `backend`     | `wedding_api`     | 8000  | API FastAPI (HTTPS)                    |
| `frontend`    | `wedding_ui`      | 5173  | App Vue/Vite (HTTPS)                   |
| `adminer`     | `wedding_adminer` | 8080  | Interface web pour inspecter la BDD    |

Le frontend (navigateur) parle à l'API en **HTTPS** ; l'API parle à PostgreSQL sur le réseau Docker interne.

---

## Stack technique

| Couche          | Technologies                                                        |
|-----------------|---------------------------------------------------------------------|
| Frontend        | Vue 3 (Composition API), Vite, Tailwind CSS 4, Vue Router, Pinia, Axios |
| Backend         | FastAPI, SQLAlchemy 2, Pydantic v2, Uvicorn                         |
| Base de données | PostgreSQL 15                                                       |
| Auth            | JWT (access + refresh, `python-jose`) + Google OAuth via Firebase   |
| Paiement        | Stripe Checkout (+ webhook)                                          |
| Stockage médias | AWS S3 — avec **repli local** (`/uploads`) si S3 non configuré      |
| Images          | Pillow (optimisation/redimensionnement à l'upload)                  |
| TLS dev         | mkcert (certificats locaux approuvés)                               |
| CI/CD           | GitHub Actions                                                      |

---

## Fonctionnalités

- **Galerie de templates** — 14 designs répartis en 4 univers : *Luxe Minimaliste*, *Classique Royal*, *Art & Culture*, *Bohème Chic*.
- **Onboarding** (`MagicWizard`) — wizard en 4 étapes : prénoms → date → lieu → style.
- **Éditeur de carte** — thème (couleurs, polices, tailles), contenu, blocs déplaçables (hero, compte à rebours, programme, RSVP, texte libre, footer), image, musique, page de garde animée. Aperçu live mobile/desktop, historique undo/redo.
- **Page publique** — URL partageable `/cards/:slug` (et lien court `/i/:slug`), plein écran, responsive, avec aperçu de partage (Open Graph).
- **RSVP public** — les invités répondent depuis l'invitation (présence, +1, régime, message) ; la réponse remonte dans l'espace des mariés.
- **Gestion des invités** — ajout, statuts, accompagnants, recherche/filtre, export CSV (premium).
- **Plan de table** — création de tables, attribution glisser-déposer (et menu tactile sur mobile), jauge de remplissage.
- **Compte à rebours** — décompte live jusqu'au jour J.
- **Forfaits** — `classic` et `premium` (montée en gamme via Stripe).
- **Espace admin** — liste des utilisateurs, statistiques, activation/désactivation de comptes.

---

## Modèle de données

```
User ──< Event ──1:1── Card ──< SubEvent   (étapes du programme)
  │         │             └──< CardVersion  (historique de l'éditeur)
  │         ├──< Guest ──< RSVP
  │         └──< WeddingTable >──< Guest    (N:N — affectation aux tables)
  │
CardTemplate   (catalogue global des 14 templates, indépendant des users)
```

| Modèle         | Rôle                                                                          |
|----------------|-------------------------------------------------------------------------------|
| `User`         | Compte. `plan` (`classic`/`premium`), `is_admin`, `is_active`.                |
| `Event`        | Un mariage. Appartient à un `User` ; porte noms, date, lieu.                  |
| `Card`         | L'invitation (1:1 avec `Event`). `config_json` (tout le design), `slug` public, `is_published`, `media_url`, `music_url`. |
| `CardTemplate` | Template du catalogue. `id` (slug), `manifest_json` (config par défaut), `category`, `required_plan`. |
| `SubEvent`     | Une étape du programme (titre, heure).                                        |
| `CardVersion`  | Snapshot d'historique de l'éditeur.                                           |
| `Guest`        | Invité. `rsvp_status`, `parent_id` (accompagnants).                           |
| `RSVP`         | Trace d'une réponse publique.                                                 |
| `WeddingTable` | Table du plan de salle, reliée aux invités (N:N).                            |

> Détails des colonnes : [`backend/app/models/wedding.py`](backend/app/models/wedding.py).

---

## Forfaits (plans)

Définis dans [`backend/app/api/plans.py`](backend/app/api/plans.py) et **appliqués côté serveur** (pas seulement dans l'UI).

| Capacité                     | `classic` (29 €) | `premium` (79 €) |
|------------------------------|:----------------:|:----------------:|
| Pages max                    | 3                | 20               |
| Sites d'invitation max       | 1                | 5                |
| Page de garde + RSVP         | ✅               | ✅               |
| Plan de table                | ✅               | ✅               |
| Blocs `countdown` / `program`| ❌               | ✅               |
| Musique de fond              | ❌               | ✅               |
| Typographie personnalisée    | ❌               | ✅               |
| Export CSV des invités       | ❌               | ✅               |

La **montée en gamme** Classic → Premium ne facture que la **différence (50 €)** via `create-upgrade-session`. La rétrogradation et le re-paiement d'un forfait déjà détenu sont **refusés côté serveur**.

---

## Sécurité

- **Authentification** : tout endpoint protégé exige un JWT `Authorization: Bearer`. Un compte **désactivé** (`is_active = false`) est rejeté même avec un token encore valide.
- **Isolation des données (anti-IDOR)** : chaque accès à une carte / événement / invité / table vérifie `owner_id == utilisateur courant`. Impossible de lire ou modifier les données d'autrui en changeant un ID dans l'URL.
- **Routes admin** : `is_admin` est vérifié **côté serveur** (le garde de route front est cosmétique).
- **Gating des forfaits** : blocs premium, musique, export CSV, templates premium, limites de pages — tout est ré-imposé par l'API.
- **Paiement** : le `plan` n'est mis à jour que via une **session Stripe réellement payée** (ou le webhook signé). Trafiquer l'URL `?plan=premium` est sans effet. Garde anti double-paiement et anti-rejeu.
- **Navigation** : le garde Vue Router protège les routes (y compris au bouton « retour ») et empêche un utilisateur connecté de revenir sur les pages de connexion/inscription.

> ⚠️ **Production** : définir un `SECRET_KEY` fort (la valeur de dev `mdp123` est forgeable), des clés Stripe réelles, et un `authDomain` Firebase sur votre propre domaine (sinon Safari bloque le login Google — limitation navigateur, pas du code).

---

## HTTPS en développement local (important)

Le backend **et** le frontend sont servis en **HTTPS** (certificats mkcert). Conséquence : trois URLs doivent rester en `https://`, sinon le navigateur reçoit une réponse vide (`ERR_EMPTY_RESPONSE`) :

| Variable        | Valeur dev               | Utilité                                          |
|-----------------|--------------------------|--------------------------------------------------|
| `VITE_API_URL`  | `https://localhost:8000` | Le front appelle l'API                           |
| `BACKEND_URL`   | `https://localhost:8000` | URLs des médias uploadés (`/uploads/...`)        |
| `FRONTEND_URL`  | `https://localhost:5173` | Redirections de retour Stripe                    |

Ces valeurs ont des défauts corrects et sont injectées par `docker-compose.yaml`. Voir [LAUNCH.md](LAUNCH.md) pour la génération des certificats.

---

## URLs locales

| Service         | URL                          |
|-----------------|------------------------------|
| Frontend        | https://localhost:5173       |
| API             | https://localhost:8000       |
| Docs API (Swagger) | https://localhost:8000/docs |
| Adminer (BDD)   | http://localhost:8080        |

## Comptes de test

| Email                | Mot de passe  | Plan    | Admin |
|----------------------|---------------|---------|-------|
| `marie@classic.com`  | `password123` | classic | Non   |
| `thomas@premium.com` | `password123` | premium | Non   |
| `admin@wedding.com`  | `password123` | premium | Oui   |
