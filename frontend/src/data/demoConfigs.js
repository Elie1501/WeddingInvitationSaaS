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
  'wabi-sabi': {
    name: 'Wabi-Sabi', isPremium: true,
    layout: 'wabi-sabi',
    sections: FULL_SECTIONS,
    theme: { background: '#F7F4EE', accent: '#C4718A', text: '#2C2416', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=1200' },
    media: { image_url: 'https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'noir-eternel': {
    name: 'Noir Éternel', isPremium: false,
    layout: 'noir-eternel',
    sections: FULL_SECTIONS,
    theme: { background: '#0A0A0A', accent: '#C5A059', text: '#F5F0E8', fontFamily: 'Playfair Display', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'japonais': {
    name: 'Japonais', isPremium: false,
    layout: 'japonais',
    sections: FULL_SECTIONS,
    theme: { background: '#F8F5F0', accent: '#8B6C42', text: '#2A2016', fontFamily: 'Noto Serif JP', titleSize: '3rem' },
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
  'couture': {
    name: 'Haute Couture', isPremium: true,
    layout: 'couture',
    sections: FULL_SECTIONS,
    theme: { background: '#FAF8F5', accent: '#B5A18A', text: '#1A1612', fontFamily: 'Cormorant Garamond', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1520854221256-17451cc331bf?w=1200', image_url_2: 'https://images.unsplash.com/photo-1606216794079-73d0b3eb5d8c?w=1200' },
    media: { image_url: 'https://images.unsplash.com/photo-1520854221256-17451cc331bf?w=1200', music_url: '', splash_url: '' },
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
  'editorial': {
    name: 'Éditorial', isPremium: true,
    layout: 'editorial',
    sections: FULL_SECTIONS,
    theme: { background: '#F9F9F7', accent: '#1A1A1A', text: '#1A1A1A', fontFamily: 'Jost', titleSize: '3.5rem' },
    content: { ...BASE, image_url: 'https://images.unsplash.com/photo-1606216794079-73d0b3eb5d8c?w=1200' },
    media: { image_url: 'https://images.unsplash.com/photo-1606216794079-73d0b3eb5d8c?w=1200', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'jardin-celeste': {
    name: 'Jardin Céleste', isPremium: false,
    layout: 'jardin-celeste',
    sections: FULL_SECTIONS,
    theme: { background: '#F5F0F8', accent: '#7B5E8A', text: '#2A1E30', fontFamily: 'Playfair Display', titleSize: '3.5rem' },
    content: { ...BASE },
    media: { image_url: '', music_url: '', splash_url: '' },
    show_countdown: true, show_splash: false,
  },
  'empire-abstrait': {
    name: 'Empire Abstrait', isPremium: true,
    layout: 'empire-abstrait',
    sections: FULL_SECTIONS,
    theme: { background: '#F2EDE8', accent: '#C5855A', text: '#1C1410', fontFamily: 'Syne', titleSize: '3.5rem' },
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
};

// Liste ordonnée pour la section landing (6 templates en vedette)
export const LANDING_TEMPLATES = [
  { id: 'riviera-blanche', name: 'Riviera Blanche', isPremium: false },
  { id: 'velvet-noir',     name: 'Velvet Noir',     isPremium: true  },
  { id: 'gatsby',          name: 'Art Déco',         isPremium: true  },
  { id: 'celestial',       name: 'Céleste',          isPremium: true  },
  { id: 'wabi-sabi',       name: 'Wabi-Sabi',        isPremium: true  },
  { id: 'noir-eternel',    name: 'Noir Éternel',     isPremium: false },
];

// Config miniature : sections réduite au hero, splash désactivé
export function getThumbConfig(templateId) {
  const base = DEMO_CONFIGS[templateId];
  if (!base) return null;
  return { ...base, sections: ['hero'], show_splash: false, show_countdown: false };
}
