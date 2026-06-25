# Frontend — Documentation technique

SPA **Vue 3** (Composition API) : landing, onboarding, galerie de templates, éditeur de carte, gestion des invités, plan de table, vue publique de l'invitation et espace admin.

> Vue d'ensemble : [../README.md](../README.md) · Démarrage : [../LAUNCH.md](../LAUNCH.md)

---

## Stack

| Outil        | Version | Rôle                            |
|--------------|---------|---------------------------------|
| Vue 3        | 3.5     | Framework UI (Composition API)  |
| Vite         | 8       | Build + dev server (**HTTPS**)  |
| Tailwind CSS | 4       | Styles utilitaires              |
| Vue Router   | 5       | Navigation SPA + gardes         |
| Pinia        | 3       | State management (auth)         |
| Axios        | 1.13    | Appels HTTP (+ intercepteurs)   |
| Firebase     | 12      | Login Google                    |

---

## Structure

```
frontend/
├── index.html                 HTML racine + balises Open Graph (aperçu de partage)
├── vite.config.js             Config Vite : HTTPS mkcert, alias @, proxy
├── certs/                     Certificats mkcert (gitignorés)
├── .env.example               Modèle de variables (VITE_*)
└── src/
    ├── main.js                Point d'entrée (Vue + Pinia + Router)
    ├── App.vue                Racine
    ├── firebase.js            Init Firebase (authDomain, provider Google)
    ├── router/index.js        Routes + garde beforeEach (auth, admin, redirections)
    ├── stores/
    │   └── auth.js            Pinia : token/refresh/user, login, signup, Google, logout
    ├── service/
    │   ├── api.js             Axios (baseURL = VITE_API_URL) + injection du Bearer + refresh auto sur 401
    │   ├── plans.js           Infos/limites d'affichage par forfait
    │   └── colorUtils.js      Couleur de texte contrastée selon le fond
    ├── composables/
    │   ├── useCardStyle.js    Variables de style dérivées du thème
    │   └── useTemplateData.js  Données dérivées (compte à rebours live, etc.)
    ├── data/
    │   └── demoConfigs.js     Configs de démo + LANDING_TEMPLATES (galerie d'accueil)
    ├── components/
    │   ├── GoogleLoginButton.vue   Bouton Google (popup + repli redirect Safari)
    │   ├── MagicWizard.vue         Onboarding 4 étapes (prénoms, date, lieu, style)
    │   ├── UpgradeModal.vue        Modale d'upgrade Premium (50 €)
    │   ├── PricingCards.vue        Comparatif des forfaits
    │   ├── SocialProofBanner.vue   Bandeau « avis » de la landing
    │   └── card/                    Rendu des invitations (voir plus bas)
    └── views/
        ├── LandingView.vue          Accueil public
        ├── LoginView.vue            Connexion (email + Google)
        ├── RegisterView.vue         Inscription (+ choix forfait → Stripe)
        ├── DashboardView.vue        Tableau de bord (événements, forfait, partage)
        ├── TemplateGalleryView.vue  Galerie filtrable
        ├── CardEditorView.vue       Éditeur complet
        ├── PublicCardView.vue       Invitation publique (/cards/:slug, /i/:slug)
        ├── DemoCardView.vue         Aperçu démo d'un template (/demo/:slug)
        ├── GuestManagementView.vue  Invités + RSVP
        ├── TableManagementView.vue  Plan de table
        ├── AdminUsersView.vue       Admin — utilisateurs
        └── AdminStatsView.vue       Admin — statistiques
```

---

## Routes & garde de navigation (`router/index.js`)

| Route                 | Vue                  | Accès        | Description                  |
|-----------------------|----------------------|--------------|------------------------------|
| `/`                   | LandingView          | public       | Accueil                      |
| `/login`              | LoginView            | invité*      | Connexion                    |
| `/register`           | RegisterView         | invité*      | Inscription                  |
| `/onboarding`         | MagicWizard          | 🔒           | Wizard de création           |
| `/events/create`      | MagicWizard          | 🔒           | Création d'événement         |
| `/dashboard`          | DashboardView        | 🔒           | Tableau de bord              |
| `/templates`          | TemplateGalleryView  | 🔒           | Galerie                      |
| `/cards/edit/:id`     | CardEditorView       | 🔒           | Éditeur                      |
| `/events/:id/guests`  | GuestManagementView  | 🔒           | Invités                      |
| `/events/:id/tables`  | TableManagementView  | 🔒           | Plan de table                |
| `/admin/users`        | AdminUsersView       | 🔒 👑        | Admin utilisateurs           |
| `/admin/stats`        | AdminStatsView       | 🔒 👑        | Admin statistiques           |
| `/cards/:slug` · `/i/:slug` | PublicCardView | public       | Invitation publique          |
| `/demo/:slug`         | DemoCardView         | public       | Aperçu démo                  |

\* La garde `beforeEach` :
- redirige vers `/login` toute route `meta.requiresAuth` sans token (y compris au bouton **retour**) ;
- bloque les routes `meta.requiresAdmin` pour les non-admins ;
- **redirige les utilisateurs déjà connectés** hors de `/login` et `/register`.

> Ces gardes sont une commodité d'UX — la vraie autorisation est imposée par le **backend**.

---

## Détail de chaque page (vue par vue)

Pour chaque vue : son rôle, les **appels API** qu'elle déclenche et sa **logique** clé.

### `/` — `LandingView.vue` (public)
Page d'accueil commerciale. **Aucun appel API** : la galerie d'aperçu s'appuie sur `data/demoConfigs.js` (`LANDING_TEMPLATES`).
- Hero avec **mot animé qui tourne** (`passion.`/`élégance.`/`émotion.`).
- CTA « Créer mon invitation » → `/templates` si déjà connecté, sinon `/register`.
- Cartes de forfaits (Classic/Premium) et vignettes de templates → `/demo/:slug`.

### `/login` — `LoginView.vue` (invité)
Connexion. Logique dans `stores/auth.js` (pas d'appel API direct dans la vue).
- **Email/mot de passe** : `auth.login()` → `POST /auth/login`.
- **Google** : `auth.loginWithGoogle()` (popup, repli redirect Safari/iOS) ; `finishGoogleRedirect()` au montage finalise le retour.
- Après succès → `/admin/users` si admin, sinon `/dashboard`.

### `/register` — `RegisterView.vue` (invité)
Inscription. `auth.register()` → `POST /auth/signup` puis login automatique.
- Accepte une query `?template=slug` (venant d'un aperçu démo) pour pré-sélectionner un design.
- Après inscription → `/choose-plan` (**paywall strict** : un nouveau compte démarre sans forfait).

### `/choose-plan` — `ChoosePlanView.vue` 🔒
Sélection obligatoire d'un forfait avant tout accès produit.
- `POST /payments/create-checkout-session { plan_name }` → **redirection vers Stripe Checkout**.
- Le retour de paiement atterrit sur le dashboard (`?payment_success=true`) qui confirme la session.

### `/dashboard` — `DashboardView.vue` 🔒
Tableau de bord principal.
- `GET /events/` — liste **tous** les événements du compte (jusqu'à `max_sites` : 1 en Classic, 5 en Premium).
- **Créer un événement** : pose un flag `create_new_event` puis va au wizard → galerie, qui crée alors un **nouvel** événement (≠ réutiliser l'existant). À la limite du forfait : message clair (passer Premium **ou** supprimer un événement pour libérer un emplacement).
- Par événement : éditer (`/cards/edit/:cardId`), publier (`POST /cards/:id/publish`), gérer invités (`/events/:id/guests`), plan de table (`/events/:id/tables`), supprimer (`DELETE /events/:id`).
- **Upgrade** Classic→Premium : `POST /payments/create-upgrade-session` ; nouvel achat : `POST /payments/create-checkout-session`.
- **Confirmation Stripe** au retour : `POST /payments/confirm-payment { session_id }` (lit `?payment_success` / `session_id`).
- **Partage natif** (`navigator.share`) avec message personnalisé (noms + date).

### `/templates` — `TemplateGalleryView.vue` 🔒
Galerie filtrable par univers (Luxe Minimaliste, Classique Royal, Art & Culture, Bohème Chic).
- `GET /templates/` — catalogue actif ; `GET /events/` — pour la limite de sites.
- Sélection d'un template → si flag `create_new_event` (depuis le Dashboard) **ou** aucun événement : `POST /events/` (crée l'événement **et** sa carte) ; sinon (onboarding) réutilise le dernier événement → `/cards/edit/:id`.

### `/cards/edit/:id` — `CardEditorView.vue` 🔒
Cœur de l'application — éditeur visuel.
- `GET /cards/:id` au montage ; **auto-save debouncé** `PUT /cards/:id/save` ; `POST /cards/:id/publish`.
- `POST /events/admin/sync-cards-data` (resync nom/date/lieu dans la config — limité à ses propres cartes).
- Onglets **Garde / Contexte / Design / Structure / Médias**, **undo/redo**, aperçu **mobile ⇄ desktop**, et sur mobile bascule **plein écran Éditer ⇄ Aperçu**.
- **Clic sur un bloc dans l'aperçu** → bascule directement vers ses champs d'édition (+ focus du 1er champ).
- Onglet Médias → **Partage (⭐ premium)** : **QR code** (lib `qrcode`, généré côté client, téléchargeable) et **URL personnalisée** (`PATCH /cards/:id/slug`). Musique d'ambiance disponible **tous forfaits**.
- Le rendu passe par `components/card/CardRenderer.vue` (voir plus bas).

### `/events/:id/guests` — `GuestManagementView.vue` 🔒
Gestion de la liste d'invités.
- `GET /guests/event/:id` ; `POST /guests` ; `PATCH /guests/:id` (statut RSVP) ; `DELETE /guests/:id`.
- Recherche/filtre par nom et par statut ; gestion des accompagnants (`parent_id`).
- **Tableau de bord RSVP temps réel** : confirmés / absents / total + récap des **régimes alimentaires** (agrégés depuis la liste, tous forfaits).
- **Export CSV** (⭐ premium) : `GET /guests/event/:id/export/csv` (`responseType: 'blob'`).

### `/events/:id/tables` — `TableManagementView.vue` 🔒
Plan de salle.
- `GET /tables/event/:id` + `GET /guests/event/:id` ; `POST /tables` ; `DELETE /tables/:id`.
- **Affectation glisser-déposer** : `POST /tables/:id/assign/:guestId` / `…/unassign/:guestId`.
- **Export CSV** (⭐ premium) : `GET /tables/event/:id/export/csv` (`responseType: 'blob'`).

### `/cards/:slug` · `/i/:slug` — `PublicCardView.vue` (public)
Invitation publique partagée aux invités.
- `GET /events/public/card/:slug` — **DTO public filtré** (aucune donnée privée du back-office).
- Affiche la carte plein écran + le **formulaire RSVP** (qui poste sur `POST /guests/public/rsvp`).
- **Musique d'ambiance** jouée chez l'invité (démarrée au clic « Entrer » de la page de garde, bouton flottant lecture/pause).
- Bouton **« Ajouter au calendrier » (.ics)** généré côté client — affiché si le propriétaire est **Premium** (`owner_plan`).
- Carte non publiée → 404 (sauf le propriétaire qui peut prévisualiser).

### `/demo/:slug` — `DemoCardView.vue` (public)
Aperçu d'un template sans compte (données factices via `demoConfigs.js`). CTA → `/register?template=slug`.

### `/admin/users` — `AdminUsersView.vue` 🔒 👑
- `GET /users/` ; `PATCH /users/:id/status` (activer/désactiver) ; `DELETE /users/:id`.

### `/admin/stats` — `AdminStatsView.vue` 🔒 👑
- `GET /users/stats` — KPI business (MRR, ARR, taux de conversion, churn, cartes/mois).

### `/dev/templates` — `dev/TemplateQAView.vue` (DEV uniquement)
Banc de QA visuel des templates ; `beforeEnter` redirige vers `/` hors mode développement.

---

## Authentification (`stores/auth.js` + `service/api.js`)

- JWT `token` + `refresh_token` stockés dans `localStorage` ; `user` hydraté de façon synchrone au chargement.
- Axios injecte `Authorization: Bearer <token>` à chaque requête ; sur **401**, l'intercepteur tente un refresh automatique avant d'abandonner.
- **Google** : `signInWithPopup` (Chrome) avec **repli `signInWithRedirect`** sur Safari/iOS (l'ITP bloque la popup) ; le retour est finalisé par `finishGoogleRedirect()` sur Login/Register. L'`idToken` Firebase est échangé contre nos JWT côté backend.

---

## Moteur de rendu des cartes (`components/card/CardRenderer.vue`)

Cœur de l'affichage : reçoit un objet `config` (JSON) et rend dynamiquement les **sections** dans l'ordre de `config.sections`.

**Sections** (`CardSection*` / blocs) :

| ID                | Composant                  |
|-------------------|----------------------------|
| `hero` / `*-full` | template hero (selon `config.layout`) |
| `countdown`       | `CardSectionCountdown` (libellés en couleur d'accent) |
| `program`         | `CardSectionProgramme`     |
| `rsvp`            | `CardSectionRSVP` (formulaire public) |
| `custom-text-*`   | `CardSectionText`          |
| `footer`          | pied de page               |

`CardSplashScreen` = page de garde animée (affichée avant l'invitation si `show_splash`). `CardCountdown` = décompte utilisé sur le splash.

**Templates hero** (`config.layout` → composant), les 14 du catalogue :

| `layout`                  | Composant                  | Univers          |
|---------------------------|----------------------------|------------------|
| `tel-aviv`                | CardTemplateTelAviv        | Classique Royal  |
| `riviera-blanche`         | CardTemplateRivieraBlanche | Luxe Minimaliste |
| `velvet-noir`             | CardTemplateVelvetNoir     | Luxe Minimaliste |
| `ora`                     | CardTemplateOra            | Luxe Minimaliste |
| `eclipse`                 | CardTemplateEclipse        | Luxe Minimaliste |
| `amour`                   | CardTemplateAmour          | Luxe Minimaliste |
| `gatsby`                  | CardTemplateGatsby         | Classique Royal  |
| `cinema`                  | CardTemplateCinema         | Classique Royal  |
| `empire-abstrait`         | CardTemplateEmpireAbstrait | Art & Culture    |
| `celestial`               | CardTemplateCelestial      | Art & Culture    |
| `film` / `typography-focus` | CardTemplateFilm         | Art & Culture    |
| `riviera` / `split`       | CardTemplateRiviera        | Bohème Chic      |
| `jardin-celeste`          | CardTemplateJardinCeleste  | Bohème Chic      |
| `japonais` / `arch`       | CardTemplateJaponais       | Bohème Chic      |

### Mode éditeur vs public
`CardRenderer` reçoit `isEditorMode` via `provide/inject`.
- **Éditeur** : clic sur une section → `emit('select-block', id)` → panneau de config.
- **Public** : pas de surbrillance, page de garde si `config.show_splash`.

---

## Éditeur (`CardEditorView.vue`)

Onglets : **Garde** (splash), **Contexte** (bloc sélectionné — atteint en cliquant un bloc dans l'aperçu, avec focus du 1er champ), **Design** (couleurs/polices), **Structure** (blocs déplaçables), **Médias** (image, musique d'ambiance, **Partage : QR code + URL personnalisée** ⭐). Aperçu live (mobile/desktop), historique undo/redo, auto-save (debounce). Un compte **Classic** ne reçoit jamais de bloc premium par défaut. Sur mobile : aperçu en haut, éditeur en bas.

---

## Partage (Open Graph)

`index.html` porte des balises **Open Graph / Twitter Card** : tout lien partagé (WhatsApp, iMessage, etc.) affiche une vignette de marque. Le dashboard génère en plus un message de partage personnalisé (noms + date) et propose le **partage natif** (`navigator.share`).

---

## Configuration (`.env`)

| Variable        | Défaut                    | Rôle                 |
|-----------------|---------------------------|----------------------|
| `VITE_API_URL`  | `https://localhost:8000`  | URL de l'API (**https** obligatoire — voir LAUNCH) |
| `VITE_FIREBASE_*` | —                       | Config Firebase (login Google) |

Modèle complet : [`.env.example`](.env.example).

---

## Commandes

```bash
npm install      # dépendances
npm run dev      # dev server (HTTPS si certs présents)
npm run build    # build de production (dist/)
npm run preview  # prévisualiser le build
```

---

## Tests / qualité

Le frontend n'a **pas de suite de tests unitaires** (pas de Vitest/Jest). Le garde-fou qualité est le **build** : la compilation Vue/Vite échoue sur toute erreur de syntaxe ou d'import, ce qui suffit à bloquer un code cassé.

```bash
cd frontend
npm run build    # doit réussir — c'est le gate de la CI
```

C'est exactement ce que joue le job **`frontend-ci`** (`.github/workflows/main.yml`) : si `npm run build` échoue, la PR ne peut pas être mergée. À lancer systématiquement avant de pousser.

> Astuce : `npm run preview` après un build sert à vérifier le rendu réel du bundle de production.
