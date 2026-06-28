# EC09 — Guide de bonnes pratiques

**Projet :** WeddingInvitationSaaS — plateforme d'invitations de mariage digitales
**Binôme :** Elie Chicha & Umair Ishfaq — ORT Montreuil, 2026

Ce guide décrit les pratiques de qualité logicielle réellement appliquées sur le projet,
illustrées par des exemples tirés de notre dépôt. Pour chaque point, nous indiquons aussi
ce que nous aurions dû mettre en place plus rigoureusement.

---

## 1. Revues de code

**Ce que nous avons mis en place**

- Intégration via **Pull Requests GitHub** : une trentaine de PR (#1 à #31), chacune partant
  d'une branche dédiée puis fusionnée sur `main`
  (ex. `#26 fix/payment-double-charge-guard`, `#22 feat/open-graph-share`).
- Deux contrôles d'intégration continue **bloquants** à chaque PR (cf. §4) : si les tests
  back-end ou le build front échouent, la PR ne peut pas être mergée.
- Discussion en binôme des changements sensibles (sécurité, paiement) avant fusion.

**Ce qu'il aurait fallu faire**

- Activer la **branch protection** sur `main` exigeant **au moins une review approuvée par
  l'autre membre** avant merge — en pratique, plusieurs PR ont été auto-mergées par leur auteur.
- Interdire le **push direct** sur `main`.
- Formaliser une **checklist de revue** : tests ajoutés, aucun secret commité, doc à jour,
  impact sécurité vérifié.

---

## 2. Conventions Git & nommage

**Ce que nous avons mis en place**

- **Conventional Commits** avec scope :
  `feat(éditeur): …`, `fix(sécurité): …`, `fix(ci): …`, `docs(api): …`, `refactor: …`, `chore: …`.
- **Branches par fonctionnalité** : `feat/alerts-paywall-strict`, `fix/stripe-redirect-https`,
  `fix-ci-stripe-env`, `feat/public-invitation-responsive`…
- **Nommage du code** cohérent par langage :
    - `snake_case` en Python (`hashed_password`, `is_active`, `required_plan`) ;
    - `camelCase` en JavaScript (`useCardStyle`, `loginWithGoogle`) ;
    - `PascalCase` pour les composants Vue (`CardRenderer.vue`, `MagicWizard.vue`).
- `.gitignore` couvrant les éléments sensibles : `.env`, certificats `certs/`, dossier `uploads/`.

**Ce qu'il aurait fallu faire**

- Documenter ces conventions dans un `CONTRIBUTING.md` (elles sont restées implicites).
- Ajouter des **linters / formatters automatiques** en *pre-commit* — Ruff/Black côté Python,
  ESLint/Prettier côté Vue — pour garantir le style sans relecture manuelle.

---

## 3. Architecture modulaire

**Principe directeur : un module = une responsabilité.**

**Back-end (`backend/app/`)** — découpage en couches :

- `api/endpoints/` : **un routeur par domaine** (`auth`, `events`, `cards`, `guests`, `table`,
  `templates`, `payments`).
- `api/deps.py` : dépendances d'autorisation **centralisées** (`get_current_user`, `require_admin`,
  `require_paid_plan`, `check_plan_permission`) — injectées plutôt que recopiées dans chaque route.
- `api/plans.py` : **source de vérité unique** des limites de forfait (`PLAN_LIMITS`).
- `core/` : un utilitaire = un fichier (`security.py` JWT/hash, `csv_utils.py` anti-injection,
  `ratelimit.py`, `storage.py` S3/local).
- `models/` (ORM SQLAlchemy), `schemas/` (Pydantic), `db/session.py` :
  séparation nette données / validation / accès.

**Front-end (`frontend/src/`)** :

- `views/` (une vue par page), `components/` (dont `card/` : `CardRenderer` + `CardSection*` +
  `CardTemplate*`), `composables/` (`useCardStyle`, `useTemplateData`), `stores/` (Pinia `auth`),
  `service/` (axios `api.js`), `router/` (gardes de navigation).
- **`CardRenderer`** : moteur de rendu **piloté par les données** — il lit `config.sections` et
  rend dynamiquement chaque section ; un template ne porte que son identité visuelle,
  aucune logique dupliquée.

**Ce qu'il aurait fallu faire**

- Côté back, extraire une **couche services** explicite (logique métier) hors des endpoints,
  qui restent parfois épais.
- Fournir un **diagramme des dépendances entre modules** pour faciliter l'arrivée d'un tiers.

---

## 4. Stratégie de tests

**Ce que nous avons mis en place**

- **Back-end : 47 tests Pytest** répartis en 8 fichiers (`test_auth`, `test_login_extended`,
  `test_cards`, `test_events`, `test_guests`, `test_tables`, `test_payments`, `test_admin`).
- Tests d'**intégration de l'API sur une base de test dédiée** : SQLite en mémoire en local,
  **PostgreSQL** en CI (au plus proche de la production).
- Couverture des **règles métier critiques** : limite `max_sites` par forfait, gating Premium,
  garde anti double-paiement Stripe, règle « invité affecté à une table du même événement »,
  contrôle d'accès admin.
- **CI GitHub Actions** (`.github/workflows/main.yml`) avec trois *jobs* dont deux **bloquants** :
  `backend-ci` (pytest sur Postgres) et `frontend-ci` (`npm run build`), plus `docker-build`.
  Variables Stripe factices injectées en CI, reset du rate-limiter entre les tests.

**Ce qu'il aurait fallu faire**

- Côté **front, aucun test unitaire** (pas de Vitest/Jest) : le seul garde-fou est le build.
  Il faudrait des tests Vitest sur les composables (`useCardStyle`, `useTemplateData`) et les
  vues critiques (éditeur, RSVP).
- Mesurer et afficher une **couverture cible** (ex. 70 % back) via `pytest --cov`.
- Ajouter des tests **end-to-end** (Cypress/Playwright) sur le parcours clé :
  création → édition → publication → RSVP.

---

## 5. Documentation technique

**Ce que nous avons mis en place**

- `README.md` général (architecture, stack, modèle de données, forfaits, **section sécurité**),
  complété par `backend/README.md` et `frontend/README.md` détaillés.
- `LAUNCH.md` : démarrage pas-à-pas (Docker Compose, génération des certificats mkcert, seed).
- `API_DOC.md` : l'ensemble des routes ; **Swagger auto-généré** sur `/docs` (FastAPI).
- **Modèle de données documenté** (`User → Event → Card`, `Guest`/`RSVP`, `WeddingTable` en N:N)
  et fichiers `.env.example` côté back et front.

**Ce qu'il aurait fallu faire**

- Produire un **schéma d'architecture et de base de données visuel** (image) en plus du texte.
- Tenir un **CHANGELOG** et des **ADR** (Architecture Decision Records) pour tracer les choix
  techniques (pourquoi FastAPI, pourquoi un `config_json`, etc.).

---

## Synthèse (slide de soutenance)

| Pratique          | Mis en place                                                           | À renforcer                                  |
| ----------------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| Revues de code    | PR GitHub + CI bloquante                                               | branch protection + 1 review obligatoire     |
| Conventions Git   | Conventional Commits, branches `feat/…`, snake/camel/Pascal            | `CONTRIBUTING.md` + linters en pre-commit    |
| Architecture      | couches back (api/core/models/schemas), `CardRenderer` piloté données  | couche services explicite                    |
| Tests             | 47 tests Pytest sur base dédiée + CI 3 jobs                            | tests front (Vitest), couverture cible, E2E  |
| Documentation     | READMEs, LAUNCH, API_DOC, Swagger, modèle de données                   | schéma visuel, ADR / CHANGELOG               |
