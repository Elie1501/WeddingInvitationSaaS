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

---

## 🔐 Authentification Google (Firebase)

### 1. Configuration Frontend
1. Créez un projet sur la [Console Firebase](https://console.firebase.google.com/).
2. Activez l'authentification **Google** dans la section "Authentication".
3. Créez une "Web App" pour obtenir vos clés API.
4. Remplissez le fichier `frontend/.env` avec ces valeurs (voir `frontend/.env.example`).

### 2. Configuration Backend (Firebase Admin SDK)
Pour que le backend puisse vérifier les `idToken` envoyés par le frontend, vous devez configurer un compte de service :

1. Dans la console Firebase, allez dans **Paramètres du projet** > **Comptes de service**.
2. Cliquez sur **Générer une nouvelle clé privée**. Cela téléchargera un fichier `.json`.
3. Placez ce fichier dans le dossier `backend/` (par exemple, nommez-le `firebase-service-account.json`).
4. **Sécurité** : Ajoutez ce fichier au `.gitignore` pour ne jamais le commiter.
5. Définissez la variable d'environnement suivante dans votre système ou votre `.env` backend :
   ```env
   GOOGLE_APPLICATION_CREDENTIALS="backend/firebase-service-account.json"
   ```

### 3. Endpoint d'Authentification Google
`POST /auth/google`
- **Corps**: `{ "id_token": "string" }`
- **Description**: Échange un token Firebase contre un JWT local. Crée l'utilisateur automatiquement s'il n'existe pas.

