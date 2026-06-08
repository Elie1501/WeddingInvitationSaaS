# Wedding Invitation SaaS

Plateforme de création d'invitations de mariage digitales. Les mariés choisissent un template, personnalisent leur invitation, gèrent leurs invités et suivent les RSVP — le tout depuis une interface web.

---

## Architecture

```
WeddingInvitationSaaS/
├── backend/        FastAPI + PostgreSQL (API REST)
├── frontend/       Vue.js 3 + Tailwind CSS (SPA)
├── docker-compose.yaml
└── LAUNCH.md       Guide de démarrage
```

Le projet tourne entièrement via **Docker Compose** : 4 services (db, backend, frontend, adminer).

---

## Stack technique

| Couche      | Technologie                              |
|-------------|------------------------------------------|
| Frontend    | Vue 3, Vite, Tailwind CSS 4, Pinia, Axios |
| Backend     | FastAPI, SQLAlchemy 2, Pydantic v2       |
| Base de données | PostgreSQL 15                        |
| Auth        | JWT (access + refresh) + Google OAuth (Firebase) |
| Paiement    | Stripe                                   |
| Stockage    | AWS S3 (media/images)                    |
| CI/CD       | GitHub Actions                           |

---

## Fonctionnalités principales

- **Galerie de templates** — 16 templates répartis en 4 univers : Luxe Minimaliste, Classique Royal, Art & Culture, Bohème Chic
- **Éditeur de carte** — personnalisation du thème (couleurs, polices, tailles), contenu, galerie photos, musique de fond
- **Page publique** — URL partageable `/cards/:slug`, plein écran, adaptée mobile et desktop
- **Splash screen** — page de garde animée avant l'invitation
- **Gestion des invités** — ajout, import, statuts RSVP, +1, restrictions alimentaires
- **Plan de table** — attribution des invités aux tables, calcul des places
- **Décompte** — compteur live jusqu'à la date du mariage
- **Plans** — `classic` (gratuit) et `premium` avec Stripe

---

## URLs locales

| Service   | URL                      |
|-----------|--------------------------|
| Frontend  | http://localhost:5173    |
| API       | http://localhost:8000    |
| Docs API  | http://localhost:8000/docs |
| Adminer   | http://localhost:8080    |

---

## Comptes de test

| Email                 | Mot de passe | Plan    | Admin |
|-----------------------|--------------|---------|-------|
| marie@classic.com     | password123  | classic | Non   |
| thomas@premium.com    | password123  | premium | Non   |
| admin@wedding.com     | password123  | premium | Oui   |

> Voir [LAUNCH.md](LAUNCH.md) pour démarrer le projet.
