# 📡 Documentation de l'API — Wedding Invitation SaaS

API REST de la plateforme d'invitations de mariage. Ce document décrit **toutes les routes**, l'authentification, les conventions, les codes d'erreur et le gating par forfait.

> 🔎 **Documentation interactive (Swagger UI)** : <https://localhost:8000/docs> — schémas exacts, essais en direct.
> 📘 Vue d'ensemble : [README.md](README.md) · Backend : [backend/README.md](backend/README.md)

---

## Sommaire

- [Bases](#bases)
- [Authentification](#authentification)
- [Conventions & légende](#conventions--légende)
- [Codes d'erreur](#codes-derreur)
- [Limites de débit (rate-limiting)](#limites-de-débit-rate-limiting)
- [Forfaits & gating](#forfaits--gating)
- [Routes](#routes)
  - [`/auth` — Authentification](#auth--authentification)
  - [`/users` — Administration](#users--administration-)
  - [`/events` — Événements](#events--événements)
  - [`/cards` — Cartes / invitations](#cards--cartes--invitations)
  - [`/guests` — Invités & RSVP](#guests--invités--rsvp)
  - [`/tables` — Plan de table](#tables--plan-de-table)
  - [`/templates` — Catalogue](#templates--catalogue)
  - [`/payments` — Paiement (Stripe)](#payments--paiement-stripe)

---

## Bases

| | |
|---|---|
| **Base URL (dev)** | `https://localhost:8000` |
| **Préfixe** | Aucun — les routes sont montées à la racine (ex. `POST /auth/login`). |
| **Format** | JSON (sauf `login` = `x-www-form-urlencoded`, `upload` = `multipart/form-data`, exports = `text/csv`) |
| **Encodage** | UTF-8 |
| **Auth** | JWT — en-tête `Authorization: Bearer <access_token>` |

> ⚠️ En dev, l'API est servie en **HTTPS** (certificat mkcert). Toujours appeler en `https://` — un appel `http://` renvoie une réponse vide.

---

## Authentification

L'API utilise des **JSON Web Tokens** : un `access_token` (courte durée) et un `refresh_token` (longue durée).

**1. Obtenir un token** — par email/mot de passe :

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=marie@classic.com&password=password123
```

```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

> Connexion Google : `POST /auth/google` avec `{ "id_token": "<jeton Firebase>" }`.

**2. Appeler une route protégée** — joindre le token :

```http
GET /auth/me
Authorization: Bearer eyJhbGci...
```

**3. Renouveler** quand l'`access_token` expire (réponse `401`) :

```http
POST /auth/refresh-token
Content-Type: application/json

{ "refresh_token": "eyJhbGci..." }
```

> Un compte **désactivé** (`is_active = false`) est rejeté même avec un token encore valide.

---

## Conventions & légende

Niveau d'accès indiqué pour chaque route :

| Icône | Signification |
|:-----:|---------------|
| 🌐 | **Public** — aucune authentification |
| 🔒 | **Authentifié** — token requis |
| 👑 | **Admin** — `is_admin = true` requis (`require_admin`) |
| 💳 | **Forfait payé** requis (`require_paid_plan`) |
| ⭐ | **Premium** requis (`check_plan_permission`) |

**Isolation des données (anti-IDOR)** : toute route sur une ressource (carte, événement, invité, table) vérifie côté serveur que la ressource appartient à l'utilisateur courant (`owner_id`). Changer un ID dans l'URL pour viser les données d'autrui renvoie `403`/`404`.

---

## Codes d'erreur

| Code | Sens |
|------|------|
| `200` / `201` | Succès |
| `204` | Succès sans contenu (suppression) |
| `400` | Requête invalide (règle métier — ex. table d'un autre événement) |
| `401` | Non authentifié / token invalide ou expiré |
| `402` | Forfait payé requis (paywall) |
| `403` | Accès refusé (pas le propriétaire, forfait insuffisant, non-admin) |
| `404` | Ressource introuvable (ou non publiée pour un visiteur) |
| `413` | Fichier trop volumineux (upload) |
| `415` | Type de fichier non autorisé (upload) |
| `422` | Validation du corps échouée |
| `429` | Trop de requêtes (rate-limit) |

Format d'erreur :

```json
{ "detail": "Message explicite en français." }
```

---

## Limites de débit (rate-limiting)

Par adresse IP, en mémoire (anti brute-force / anti-spam) :

| Route | Limite |
|-------|--------|
| `POST /auth/login` | 10 requêtes / 5 min |
| `POST /guests/public/rsvp` | 15 requêtes / 5 min |

Dépassement → `429 Too Many Requests`.

---

## Forfaits & gating

Le forfait (`classic` / `premium`) est **ré-imposé côté serveur** — l'UI seule ne suffit pas. Un compte non payé (`none`) n'a **aucun** accès produit.

| Capacité | `classic` | `premium` |
|----------|:---------:|:---------:|
| Sites d'invitation (`max_sites`) | 1 | 5 |
| Pages max (`max_pages`) | 3 | 20 |
| Musique d'ambiance | ✅ | ✅ |
| Plan de table | ✅ | ✅ |
| Tableau de bord RSVP | ✅ | ✅ |
| Blocs premium (countdown, program, texte, image) | ❌ | ✅ |
| Templates premium | ❌ | ✅ |
| Typographie personnalisée | ❌ | ✅ |
| Export CSV (invités + plan de table) | ❌ | ✅ |
| URL personnalisée (slug) | ❌ | ✅ |

> Détails : [`backend/app/api/plans.py`](backend/app/api/plans.py).

---

## Routes

### `/auth` — Authentification

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `POST` | `/auth/signup` | 🌐 | Créer un compte. Body : `{ email, password (≥ 8 car.) }` → `UserResponse`. |
| `POST` | `/auth/login` | 🌐 | Connexion email/mot de passe (`form-urlencoded` : `username`, `password`) → tokens. *Rate-limité.* |
| `POST` | `/auth/google` | 🌐 | Connexion Google. Body : `{ id_token }` (jeton Firebase) → tokens. |
| `POST` | `/auth/refresh-token` | 🌐 | Renouvelle l'`access_token`. Body : `{ refresh_token }`. |
| `GET` | `/auth/me` | 🔒 | Profil de l'utilisateur courant (`id, email, plan, is_admin, is_active`). |

---

### `/users` — Administration 👑

Toutes ces routes exigent un compte **administrateur**.

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/users/` | 👑 | Liste tous les utilisateurs. |
| `GET` | `/users/stats` | 👑 | Statistiques globales (comptes, forfaits, etc.). |
| `GET` | `/users/{user_id}/cards` | 👑 | Cartes d'un utilisateur donné. |
| `PATCH` | `/users/{user_id}/status` | 👑 | Activer / désactiver un compte (`is_active`). |
| `DELETE` | `/users/{user_id}` | 👑 | Supprimer un compte (`204`). Un admin **ne peut pas** se supprimer lui-même (`400`). |

---

### `/events` — Événements

Un **événement** = un mariage (noms, date, lieu). Il porte **une** carte d'invitation.

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/events/` | 🔒 | Liste **tous** les événements du compte (carte incluse). |
| `POST` | `/events/` | 🔒 💳 | Crée un événement **et** sa carte. Vérifie `max_sites` → `403` si limite atteinte. Body : `EventCreate` (`title`, `groom_name`, `bride_name`, `date`, `location`, `template_id`…). |
| `GET` | `/events/{event_id}` | 🔒 | Détail d'un événement (ownership). |
| `PUT` | `/events/{event_id}` | 🔒 | Met à jour les infos de l'événement. |
| `DELETE` | `/events/{event_id}` | 🔒 | Supprime l'événement (libère un emplacement de forfait). |
| `GET` | `/events/mine/latest` | 🔒 | Dernier événement du compte ; en crée un par défaut s'il n'en existe aucun. |
| `POST` | `/events/admin/sync-cards-data` | 🔒 | Re-synchronise noms/date/lieu dans la `config_json` de **ses** cartes. |
| `GET` | `/events/public/card/{slug}` | 🌐 | **Carte publique** par slug — DTO filtré (aucune donnée privée). Inclut `owner_plan`, `sub_events`. `404` si non publiée (sauf propriétaire). |

---

### `/cards` — Cartes / invitations

La **carte** porte tout le design dans `config_json` ; elle est publiée sur un `slug`.

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/cards/` | 🔒 | Liste ses cartes (URLs médias signées). |
| `POST` | `/cards/` | 🔒 | Crée une carte pour un événement. Body : `CardCreate` (`event_id`, `template_id`…). |
| `GET` | `/cards/{card_id}` | 🔒 | Détail d'une carte. |
| `PUT` | `/cards/{card_id}/save` | 🔒 | **Auto-save** de la config. Gating premium : refuse blocs premium / dépassement de pages pour un Classic. |
| `PUT` | `/cards/{card_id}` | 🔒 | Met à jour des champs simples de la carte. |
| `POST` | `/cards/{card_id}/publish` | 🔒 | Publie / dépublie. Génère le `slug` à la première publication. |
| `PATCH` | `/cards/{card_id}/slug` | 🔒 ⭐ | **URL personnalisée**. Body : `{ slug }` → slugifié (accents/emoji retirés) + unicité garantie (suffixe auto). |
| `POST` | `/cards/{card_id}/upload` | 🔒 | **Upload média** (`multipart` : `file`, `file_type=image\|music`). Type **et** taille validés : image ≤ 10 Mo (JPG/PNG/WEBP/GIF), audio ≤ 20 Mo (MP3/AAC/OGG/WAV/M4A). `SVG/HTML` refusés. → `{ url, key }`. |
| `GET` | `/cards/{card_id}/export` | 🔒 | Export JSON de la carte. |
| `POST` | `/cards/{card_id}/import` | 🔒 | Import JSON d'une carte. |
| `GET` | `/cards/{card_id}/versions` | 🔒 | Historique des versions de l'éditeur. |
| `POST` | `/cards/{card_id}/rollback/{version_number}` | 🔒 | Restaure une version antérieure. |
| `DELETE` | `/cards/{card_id}` | 🔒 | Supprime la carte. |

---

### `/guests` — Invités & RSVP

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/guests/event/{event_id}` | 🔒 | Invités d'un événement. Filtres optionnels : `?status=`, `?q=` (recherche nom), `?table_id=`. |
| `POST` | `/guests/` | 🔒 | Ajoute un invité principal (+ ses accompagnants). Body : `GuestCreate`. |
| `PATCH` | `/guests/{guest_id}` | 🔒 | Met à jour un invité (ex. statut RSVP). |
| `DELETE` | `/guests/{guest_id}` | 🔒 | Supprime un invité. |
| `GET` | `/guests/event/{event_id}/rsvps` | 🔒 | Historique des réponses RSVP. |
| `GET` | `/guests/event/{event_id}/export/csv` | 🔒 ⭐ | **Export CSV** des invités (BOM Excel, anti-injection de formules). |
| `POST` | `/guests/public/rsvp` | 🌐 | **RSVP public** depuis l'invitation. *Rate-limité.* Body : `PublicRSVPCreate` (`event_id`, `first_name`, `last_name`, `email?`, `presence`, `sub_guests[]`, `dietary_restrictions?`, `message?`). |

---

### `/tables` — Plan de table

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/tables/event/{event_id}` | 🔒 | Tables d'un événement (avec invités assis). |
| `POST` | `/tables/` | 🔒 | Crée une table. Body : `{ name, capacity, event_id }`. |
| `PUT` | `/tables/{table_id}` | 🔒 | Modifie une table. |
| `DELETE` | `/tables/{table_id}` | 🔒 | Supprime une table. |
| `POST` | `/tables/{table_id}/assign/{guest_id}` | 🔒 | Assoit un invité. Refuse une table d'un **autre** événement (`400`) ou pleine. |
| `POST` | `/tables/{table_id}/unassign/{guest_id}` | 🔒 | Retire un invité de la table. |
| `GET` | `/tables/event/{event_id}/export/csv` | 🔒 ⭐ | **Export CSV** du plan de table. |

---

### `/templates` — Catalogue

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `GET` | `/templates/` | 🌐 | Liste les templates actifs du catalogue (14 designs, 4 univers). |
| `GET` | `/templates/{template_id}` | 🌐 | Détail d'un template (`manifest_json`, `category`, `required_plan`). |

---

### `/payments` — Paiement (Stripe)

Le `plan` d'un compte n'est **jamais** modifié directement : uniquement via une session Stripe réellement payée ou le webhook signé.

| Méthode | Route | Accès | Description |
|---------|-------|:-----:|-------------|
| `POST` | `/payments/create-checkout-session` | 🔒 | Démarre l'achat d'un forfait. Body : `{ plan_name }` → `{ checkout_url }`. Garde anti double-paiement. |
| `POST` | `/payments/create-upgrade-session` | 🔒 | Montée Classic → Premium : facture la **différence (50 €)**. Anti re-upgrade. |
| `POST` | `/payments/confirm-payment` | 🔒 | Confirme au retour. Body : `{ session_id }` → met à jour le `plan` si la session est `paid` et appartient au compte. |
| `POST` | `/payments/webhook` | 🌐 | Webhook Stripe (signature vérifiée). Source de vérité du statut de paiement. |

---

## Exemple de bout en bout

```bash
# 1. Connexion
TOKEN=$(curl -sk -X POST https://localhost:8000/auth/login \
  -d "username=thomas@premium.com&password=password123" | jq -r .access_token)

# 2. Lister ses événements
curl -sk https://localhost:8000/events/ -H "Authorization: Bearer $TOKEN"

# 3. Définir une URL personnalisée (Premium)
curl -sk -X PATCH https://localhost:8000/cards/27/slug \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"slug":"mariage-marie-jean"}'

# 4. Exporter les invités en CSV (Premium)
curl -sk https://localhost:8000/guests/event/27/export/csv \
  -H "Authorization: Bearer $TOKEN" -o invites.csv
```

---

## Comptes de test

| Email | Mot de passe | Plan | Admin |
|-------|--------------|------|:-----:|
| `marie@classic.com` | `password123` | classic | — |
| `thomas@premium.com` | `password123` | premium | — |
| `admin@wedding.com` | `password123` | premium | ✅ |
