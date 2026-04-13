# Documentation API Wedding Invitation SaaS (v1)

## Base URL
`/api/v1`

## Authentification
La plupart des endpoints nécessitent un Header `Authorization: Bearer <token>`.
Les routes publiques sont accessibles sans authentification.

---

## 📅 Événements (Events)

### Liste des événements
`GET /events/`
- **Description**: Liste tous les mariages appartenant à l'utilisateur connecté.

### Créer un événement
`POST /events/`
- **Corps**: `EventCreate`
  - `title`: string (requis)
  - `groom_name`: string
  - `bride_name`: string
  - `date`: datetime
  - `location`: string
  - `template_id`: string (optionnel, défaut: "modern-chic")
- **Description**: Crée un événement et sa carte associée.

### Mettre à jour un événement
`PUT /events/{event_id}`
- **Corps**: `EventUpdate` (similaire à EventCreate)
- **Description**: Modifie les informations de base de l'événement.

### Supprimer un événement
`DELETE /events/{event_id}`
- **Description**: Supprime l'événement et toutes les données liées (invités, tables, carte).

### Récupérer une carte publique
`GET /events/public/card/{slug}`
- **Accès**: **Public**
- **Description**: Récupère les données publiques d'une carte (titre, mariés, date, thème, config).
- **Note**: Ne fonctionne que si la carte est publiée (`is_published=True`).

---

## 💌 Cartes (Cards)

### Liste des cartes
`GET /cards/`
- **Description**: Liste toutes les cartes de l'utilisateur.

### Publier une carte
`POST /cards/{card_id}/publish`
- **Description**: Bascule l'état de publication (`is_published`). Génère un `slug` si nécessaire.

### Mettre à jour (Sauvegarde rapide)
`PUT /cards/{card_id}/save`
- **Corps**: `CardUpdate`
- **Description**: Sauvegarde les modifications (couleurs, texte, config) sans incrémenter la version majeure.

---

## 👥 Invités (Guests)

### Liste des invités
`GET /guests/event/{event_id}`
- **Paramètres Query**:
  - `rsvp_status`: string (pending, confirmed, declined)
  - `table_id`: int
  - `search`: string (nom, prénom ou email)
- **Description**: Liste les invités avec options de filtrage et recherche.

### Résumé des réponses
`GET /guests/event/{event_id}/summary`
- **Description**: Retourne des statistiques (total présents, absents, plus-ones).

### Ajouter un invité
`POST /guests/`
- **Corps**: `GuestCreate`
- **Description**: Ajout manuel d'un invité (Back-office).

### Répondre au RSVP (Public)
`POST /guests/public/rsvp`
- **Accès**: **Public**
- **Corps**: JSON (event_id, first_name, last_name, email, presence, plus_ones, etc.)
- **Description**: Enregistre la réponse d'un invité via la page publique.
- **Note**: Nécessite que la carte soit publiée.

---

## 🍽 Tables (Tables)

### Liste des tables
`GET /table/event/{event_id}`
- **Description**: Liste toutes les tables d'un mariage.

### État de remplissage
`GET /table/event/{event_id}/status`
- **Description**: Retourne l'occupation détaillée de chaque table (nombre de places, complet/non complet).

### Créer une table
`POST /table/`
- **Corps**: `TableCreate` (name, capacity, event_id)

### Assigner un invité
`POST /table/{table_id}/assign/{guest_id}`
- **Description**: Place un invité à une table.
- **Règles**: Vérifie la capacité de la table et la cohérence de l'événement. Un invité ne peut être qu'à une seule table à la fois.

---

## 🎨 Templates

### Liste des templates
`GET /templates/`
- **Description**: Liste tous les templates de design disponibles.
