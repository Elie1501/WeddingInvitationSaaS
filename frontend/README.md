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

Onglets : **Garde** (splash), **Contexte** (bloc sélectionné), **Design** (couleurs/polices), **Structure** (blocs déplaçables), **Médias** (image/musique). Aperçu live (mobile/desktop), historique undo/redo, auto-save (debounce). Un compte **Classic** ne reçoit jamais de bloc premium par défaut. Sur mobile : aperçu en haut, éditeur en bas.

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
