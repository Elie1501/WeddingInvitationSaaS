// Données fictives partagées par toutes les previews & la page /demo/:slug
export const DEMO_EVENT = {
  groom_name: 'Hugo',
  bride_name: 'Camille',
  date: '2026-09-12T00:00:00',
  location: 'Château de la Marquise, Provence',
};

const BASE = {
  names:        'Camille & Hugo',
  monogram:     'C & H',
  date_display: '12 Septembre 2026',
  address:      'Château de la Marquise, Provence',
  intro_text:   'Nous serions honorés de votre présence pour célébrer notre union.',
  rsvp_title:   'Serez-vous des nôtres ?',
  rsvp_deadline_text: 'Réponse souhaitée avant le 1er Août.',
  footer_text:  'Fait avec amour · Camille & Hugo · 2026',
  divider_symbol: '✦',
  splash_title:      'Camille & Hugo',
  splash_top_text:   'Save the Date',
  splash_button_text: 'Entrer dans l\'invitation',
};

// Sections pour la page /demo/:slug (hero + countdown + footer, pas de RSVP → pas d'appel API)
const FULL_SECTIONS  = ['hero', 'countdown', 'footer'];
// Sections pour la miniature (hero seul)
const THUMB_SECTIONS = ['hero'];

export const DEMO_CONFIGS = {
  'riviera-blanche': {
    name: 'Riviera Blanche', isPremium: false,
    layout: 'riviera-blanche',
    sections: FULL_SECTIONS,
    theme: { background: '#FAFAF8', accent: '#2E6E8E', text: '#1C2B3A', fontFamily: 'Playfair Display', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'velvet-noir': {
    name: 'Velvet Noir', isPremium: true,
    layout: 'velvet-noir',
    sections: FULL_SECTIONS,
    theme: { background: '#1a0610', accent: '#E8B4A0', text: '#F5E8E0', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1549416878-b5a76567bec9?w=1200', dress_code: 'Tenue de soirée' },
    media: { image_url: 'https://images.unsplash.com/photo-1549416878-b5a76567bec9?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'gatsby': {
    name: 'Art Déco', isPremium: true,
    layout: 'gatsby',
    sections: FULL_SECTIONS,
    theme: { background: '#100e08', accent: '#D4A853', text: '#F5E6C8', fontFamily: 'Cinzel', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200', dress_code: 'Black tie' },
    media: { image_url: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'celestial': {
    name: 'Céleste', isPremium: true,
    layout: 'celestial',
    sections: FULL_SECTIONS,
    theme: { background: '#05050f', accent: '#F0D080', text: '#E8E0FF', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'tel-aviv': {
    name: 'Tel Aviv', isPremium: false,
    layout: 'tel-aviv',
    sections: FULL_SECTIONS,
    theme: { background: '#FBF9F4', accent: '#0038B8', text: '#1A2238', namesColor: '#16203A', countdownColor: '#0038B8', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'japonais': {
    name: 'Japonais', isPremium: false,
    layout: 'japonais',
    sections: FULL_SECTIONS,
    theme: { background: '#F7EEE3', accent: '#D14B3D', text: '#2A1E18', fontFamily: 'Shippori Mincho', titleSize: '3rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'riviera': {
    name: 'Riviera', isPremium: false,
    layout: 'riviera',
    sections: FULL_SECTIONS,
    theme: { background: '#F0EBE3', accent: '#7B9EA6', text: '#2D3436', fontFamily: 'Playfair Display', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200' },
    media: { image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'cinema': {
    name: 'Cinéma', isPremium: true,
    layout: 'cinema',
    sections: FULL_SECTIONS,
    theme: { background: '#080808', accent: '#D4853A', text: '#F0EAE0', fontFamily: 'Lato', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200', intro_text: 'Un film d\'amour dont vous êtes les héros.' },
    media: { image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'jardin-celeste': {
    name: 'Jardin Céleste', isPremium: false,
    layout: 'jardin-celeste',
    sections: FULL_SECTIONS,
    theme: { background: '#0F2419', accent: '#D9E86B', text: '#F2EBE0', fontFamily: 'Cormorant Upright', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'empire-abstrait': {
    name: 'Empire Abstrait', isPremium: true,
    layout: 'empire-abstrait',
    sections: FULL_SECTIONS,
    theme: { background: '#0E0C18', accent: '#FF6B6B', text: '#EDE9F5', namesColor: '#FFFFFF', countdownColor: '#FF6B6B', fontFamily: 'Space Grotesk', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'ora': {
    name: 'Ora', isPremium: false,
    layout: 'ora',
    sections: FULL_SECTIONS,
    theme: { background: '#FFF9F3', accent: '#D4956A', text: '#2A1A0E', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200' },
    media: { image_url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },

  'film': {
    name: 'Pellicule', isPremium: true,
    layout: 'film',
    sections: FULL_SECTIONS,
    theme: { background: '#F2E9DB', accent: '#C77F4E', text: '#3A2E24', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200', intro_text: 'Quelques instants volés, à garder pour toujours.' },
    media: { image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },

  // ── Nouveaux templates 2026 ────────────────────────────────────────────────
  // Ces templates sont auto-portants (toutes les sections incluses dans le composant).
  // sections: ['hero'] → CardRenderer délègue tout l'affichage au composant.

  'eclipse': {
    name: 'Éclipse', isPremium: true,
    layout: 'eclipse',
    sections: ['hero'],
    theme: {
      background: '#1B1430',
      accent: '#F0A85C',
      text: '#E8DFF0',
      namesColor: '#FBF3E8',
      countdownColor: '#F0A85C',
      sectionTitleColor: '#F0A85C',
      fontFamily: 'Fraunces',
    },
    content: { ...BASE },
    sub_events: [
      { time: '14h00', title: 'Cérémonie civile', location: 'Mairie de Provence' },
      { time: '16h30', title: 'Cérémonie religieuse', location: 'Chapelle Saint-Pierre', description: 'Accueil des invités à partir de 16h00.' },
      { time: '19h00', title: 'Vin d\'honneur', location: 'Terrasses du château' },
      { time: '21h00', title: 'Dîner & soirée', location: 'Grande salle du château' },
    ],
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },

  'amour': {
    name: 'Amour', isPremium: false,
    layout: 'amour',
    sections: ['hero'],
    theme: {
      background: '#FDF1F0',
      accent: '#D6677A',
      text: '#4A2E33',
      namesColor: '#6B2737',
      countdownColor: '#D6677A',
      sectionTitleColor: '#D6677A',
      fontFamily: 'Cormorant Garamond',
    },
    content: { ...BASE },
    sub_events: [
      { time: '14h00', title: 'Cérémonie civile', location: 'Mairie de Provence' },
      { time: '16h30', title: 'Cérémonie religieuse', location: 'Chapelle Saint-Pierre', description: 'Accueil des invités à partir de 16h00.' },
      { time: '19h00', title: 'Vin d\'honneur', location: 'Terrasses du château' },
      { time: '21h00', title: 'Dîner & soirée', location: 'Grande salle du château' },
    ],
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },

};

// Liste ordonnée pour la section landing (6 templates en vedette)
export const LANDING_TEMPLATES = [
  { id: 'riviera-blanche', name: 'Riviera Blanche', isPremium: false, image: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=600' },
  { id: 'velvet-noir',     name: 'Velvet Noir',     isPremium: true,  image: 'https://images.unsplash.com/photo-1549416878-b5a76567bec9?auto=format&fit=crop&q=80&w=600' },
  { id: 'gatsby',          name: 'Art Déco',         isPremium: true,  image: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=600' },
  { id: 'celestial',       name: 'Céleste',          isPremium: true,  image: 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?auto=format&fit=crop&q=80&w=600' },
  { id: 'tel-aviv',        name: 'Tel Aviv',         isPremium: false, image: 'https://images.unsplash.com/photo-1602002418082-dd4a3f5b1aef?auto=format&fit=crop&q=80&w=600' },
];

// Config miniature : sections réduite au hero, splash désactivé
export function getThumbConfig(templateId) {
  const base = DEMO_CONFIGS[templateId];
  if (!base) return null;
  return { ...base, sections: ['hero'], show_splash: false, show_countdown: false };
}
