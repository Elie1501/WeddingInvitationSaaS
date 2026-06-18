# Frontend — Documentation Technique

Application **Vue.js 3** (SPA) qui sert d'interface utilisateur complète : landing page, onboarding, galerie de templates, éditeur de carte, gestion des invités et vue publique de l'invitation.

---

## Stack

| Outil          | Version | Rôle                                  |
|----------------|---------|---------------------------------------|
| Vue 3          | 3.5     | Framework UI (Composition API)        |
| Vite           | 8       | Build tool + dev server               |
| Tailwind CSS   | 4       | Utilitaires CSS                       |
| Vue Router     | 5       | Navigation SPA                        |
| Pinia          | 3       | State management                      |
| Axios          | 1.13    | Appels HTTP vers l'API                |
| Firebase       | 12      | Authentification Google               |

---

## Structure

```
frontend/src/
├── main.js                     Point d'entrée Vue
├── App.vue                     Racine de l'app
├── router/
│   └── index.js                Toutes les routes + guards
├── stores/
│   └── auth.js                 Store Pinia : token JWT, user, login/logout
├── service/
│   ├── api.js                  Instance Axios configurée (base URL + intercepteurs)
│   ├── colorUtils.js           Calcul de couleur de texte contrastante
│   └── plans.js                Limites par plan (classic / premium)
├── firebase.js                 Config Firebase (Google Auth)
├── components/
│   ├── GoogleLoginButton.vue   Bouton connexion Google
│   ├── MagicWizard.vue         Onboarding multi-étapes (noms, date, lieu, style)
│   ├── PricingCards.vue        Tableau comparatif des plans
│   └── card/
│       ├── CardRenderer.vue    Moteur de rendu dynamique des sections
│       ├── CardSectionBanner.vue     Section hero fallback
│       ├── CardSectionText.vue       Bloc texte personnalisé
│       ├── CardSectionRSVP.vue       Formulaire RSVP public
│       ├── CardCountdown.vue         Décompte live
│       ├── CardSplashScreen.vue      Page de garde animée
│       ├── CardTemplateNoirEternel.vue
│       ├── CardTemplateRivieraBlanche.vue
│       ├── CardTemplateVelvetNoir.vue
│       ├── CardTemplateCouture.vue
│       ├── CardTemplateEmpireAbstrait.vue
│       ├── CardTemplateOra.vue
│       ├── CardTemplateGatsby.vue
│       ├── CardTemplateCinema.vue
│       ├── CardTemplateBrutaliste.vue
│       ├── CardTemplateFilm.vue
│       ├── CardTemplateEditorial.vue
│       ├── CardTemplateCelestial.vue
│       ├── CardTemplateRiviera.vue
│       ├── CardTemplateJardinCeleste.vue
│       ├── CardTemplateJaponais.vue
│       └── CardTemplateWabiSabi.vue
└── views/
    ├── LandingView.vue          Page d'accueil publique
    ├── LoginView.vue            Connexion (email + Google)
    ├── RegisterView.vue         Inscription
    ├── DashboardView.vue        Tableau de bord utilisateur
    ├── TemplateGalleryView.vue  Galerie de templates filtrable
    ├── CardEditorView.vue       Éditeur complet de la carte
    ├── PublicCardView.vue       Vue publique de l'invitation (partageable)
    ├── GuestManagementView.vue  Gestion des invités + RSVP
    ├── TableManagementView.vue  Plan de table interactif
    └── AdminUsersView.vue       Administration (admin uniquement)
```

---

## Routes

| Route                   | Vue                      | Auth requise | Description                          |
|-------------------------|--------------------------|--------------|--------------------------------------|
| `/`                     | LandingView              | Non          | Page d'accueil                       |
| `/login`                | LoginView                | Non          | Connexion                            |
| `/register`             | RegisterView             | Non          | Inscription                          |
| `/onboarding`           | MagicWizard              | Oui          | Wizard de création d'événement       |
| `/dashboard`            | DashboardView            | Oui          | Tableau de bord                      |
| `/templates`            | TemplateGalleryView      | Oui          | Galerie des templates                |
| `/cards/edit/:id`       | CardEditorView           | Oui          | Éditeur de carte                     |
| `/events/:id/guests`    | GuestManagementView      | Oui          | Gestion des invités                  |
| `/events/:id/tables`    | TableManagementView      | Oui          | Plan de table                        |
| `/cards/:slug`          | PublicCardView           | Non          | Invitation publique                  |
| `/admin/users`          | AdminUsersView           | Oui + admin  | Admin utilisateurs                   |

---

## Moteur de rendu des cartes (`CardRenderer`)

`CardRenderer.vue` est le cœur du système d'affichage. Il reçoit un objet `config` (JSON) et rend dynamiquement les sections dans l'ordre défini par `config.sections`.

### Sections disponibles

| ID de section           | Composant rendu                            |
|-------------------------|--------------------------------------------|
| `hero` / `*-hero` / `*-full` | Template hero (selon `config.layout`) |
| `countdown`             | Décompte live                              |
| `program`               | Programme des sous-événements              |
| `rsvp`                  | Formulaire RSVP                            |
| `custom-text-*`         | Bloc texte libre                           |
| `footer`                | Pied de page                               |

### Routing des templates hero

Le layout est déterminé par `config.layout` :

| Valeur de `layout`    | Template rendu                 | Catégorie         |
|-----------------------|--------------------------------|-------------------|
| `noir-eternel`        | CardTemplateNoirEternel        | Luxe Minimaliste  |
| `riviera-blanche`     | CardTemplateRivieraBlanche     | Luxe Minimaliste  |
| `velvet-noir`         | CardTemplateVelvetNoir         | Luxe Minimaliste  |
| `couture`             | CardTemplateCouture            | Luxe Minimaliste  |
| `ora`                 | CardTemplateOra                | Classique Royal   |
| `empire-abstrait`     | CardTemplateEmpireAbstrait     | Classique Royal   |
| `gatsby`              | CardTemplateGatsby             | Classique Royal   |
| `cinema`              | CardTemplateCinema             | Classique Royal   |
| `brutaliste` / `es`   | CardTemplateBrutaliste         | Art & Culture     |
| `film`                | CardTemplateFilm               | Art & Culture     |
| `editorial`           | CardTemplateEditorial          | Art & Culture     |
| `celestial`           | CardTemplateCelestial          | Art & Culture     |
| `riviera` / `split`   | CardTemplateRiviera            | Bohème Chic       |
| `jardin-celeste`      | CardTemplateJardinCeleste      | Bohème Chic       |
| `japonais` / `arch`   | CardTemplateJaponais           | Bohème Chic       |
| `wabi-sabi`           | CardTemplateWabiSabi           | Bohème Chic       |

### Thème CSS dynamique

`CardRenderer` injecte ces variables CSS sur le conteneur racine, utilisées par tous les templates :

```css
--accent        /* couleur d'accentuation */
--names-color   /* couleur des prénoms */
--names-size    /* taille des prénoms */
--title-color   /* couleur des titres de section */
--title-size    /* taille des titres */
--body-size     /* taille du corps de texte */
```

### Mode éditeur vs mode public

`CardRenderer` reçoit `isEditorMode` via `provide/inject` depuis `CardEditorView`.

- **Mode éditeur** : clic sur une section → `emit('select-block', sectionId)` → panel de config à droite
- **Mode public** : aucun ring de sélection, splash screen activé si `config.show_splash = true`

---

## Authentification

Géré par `stores/auth.js` (Pinia).

- Token JWT stocké dans `localStorage` (`token` + `refresh_token`)
- L'instance Axios dans `service/api.js` injecte automatiquement le header `Authorization: Bearer <token>` à chaque requête
- Si une requête retourne `401`, l'intercepteur tente un refresh automatique avant de rediriger vers `/login`
- Google OAuth : `signInWithPopup(Firebase)` → `idToken` Firebase → envoyé au backend → JWT interne retourné

---

## Configuration

Variables d'environnement Vite (préfixe `VITE_`) :

| Variable         | Défaut                    | Description              |
|------------------|---------------------------|--------------------------|
| `VITE_API_URL`   | `http://localhost:8000`   | URL de l'API backend     |

En développement Docker, cette valeur est injectée via `docker-compose.yaml`.

---

## Commandes

```bash
# Développement local (sans Docker)
npm install
npm run dev

# Build production
npm run build

# Preview du build de production
npm run preview
```
