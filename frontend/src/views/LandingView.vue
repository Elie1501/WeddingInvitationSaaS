<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import SocialProofBanner    from '../components/SocialProofBanner.vue';
import { LANDING_TEMPLATES } from '../data/demoConfigs.js';

const router = useRouter();
const auth   = useAuthStore();

const handleCta = () => router.push(auth.user ? '/templates' : '/register');

// ─── Cycling word ────────────────────────────────────────────────────────────
const heroWordIndex = ref(0);
const heroWords     = ['élégance', 'passion', 'émotion'];
let   wordTimer     = null;

// ─── Scroll-reveal (sections génériques) ─────────────────────────────────────
const visible   = ref(new Set());
const isVisible = (s) => visible.value.has(s);
let   revealIO  = null;

// ─── Navbar ───────────────────────────────────────────────────────────────────
// Invisible tant que le hero est dans le viewport, sinon fond blanc
const heroInView = ref(true);
const navVisible = computed(() => !heroInView.value);
const menuOpen   = ref(false);
let   heroIO     = null;

// ─── Forfaits ──────────────────────────────────────────────────────────────────
const plans = [
  {
    id: 'classic',
    name: 'Classic',
    price: '29',
    tagline: "L'essentiel pour un mariage élégant.",
    features: ["1 site d'invitation", 'Formulaire RSVP', 'Plan de table interactif', "Musique d'ambiance", 'Personnalisation complète'],
    highlight: false,
  },
  {
    id: 'premium',
    name: 'Premium',
    price: '79',
    tagline: "L'expérience complète, sans limite.",
    features: ['Tout le Classic', "Jusqu'à 5 sites d'invitation", 'Tous les templates Premium', 'Blocs de personnalisation Premium', 'Typographie personnalisée', 'Export CSV des invités'],
    highlight: true,
  },
];

// ─── Steps ───────────────────────────────────────────────────────────────────
const steps = [
  { number: '01', title: 'Choisissez votre design',    description: '18 templates exclusifs, des plus classiques aux plus avant-gardistes.' },
  { number: '02', title: 'Personnalisez chaque détail', description: 'Textes, couleurs, photos, musique — un éditeur visuel sans compétence requise.' },
  { number: '03', title: 'Partagez & organisez',        description: 'Un lien unique. RSVP automatiques, gestion des tables, zéro papier.' },
];

// ─── Lifecycle ───────────────────────────────────────────────────────────────
onMounted(() => {
  wordTimer = setInterval(() => {
    heroWordIndex.value = (heroWordIndex.value + 1) % heroWords.length;
  }, 2800);

  // Scroll-reveal pour les sections
  revealIO = new IntersectionObserver(
    (entries) => entries.forEach(e => {
      if (e.isIntersecting)
        visible.value = new Set([...visible.value, e.target.dataset.section]);
    }),
    { threshold: 0.12 }
  );
  document.querySelectorAll('[data-section]').forEach(el => revealIO.observe(el));

  // Navbar — disparaît tant que le hero est visible, réapparaît dès qu'il sort
  const heroEl = document.getElementById('hero-section');
  if (heroEl) {
    heroIO = new IntersectionObserver(
      ([entry]) => { heroInView.value = entry.isIntersecting; },
      { threshold: 0.05 }
    );
    heroIO.observe(heroEl);
  }
});

onUnmounted(() => {
  if (wordTimer)   clearInterval(wordTimer);
  revealIO?.disconnect();
  heroIO?.disconnect();
});
</script>

<template>
  <div class="min-h-screen bg-white font-sans">

    <!-- ─── NAVBAR ──────────────────────────────────────────────────────────── -->
    <nav class="fixed top-0 inset-x-0 z-50 transition-all duration-300
                bg-white/95 backdrop-blur-xl shadow-sm border-b border-primary-100"
         :class="navVisible ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0 pointer-events-none'">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        <!-- Logo -->
        <h1 class="text-lg font-serif italic text-neutral-900">
          Saas Wedding
        </h1>

        <!-- Liens desktop -->
        <div class="hidden md:flex items-center gap-8">
          <a v-for="[href, label] in [['#concept','Comment ça marche'],['#modeles','Designs'],['#avis','Avis']]"
             :key="href" :href="href"
             class="text-[10px] font-bold uppercase tracking-[0.25em] text-neutral-400 hover:text-neutral-900 transition-colors">
            {{ label }}
          </a>
        </div>

        <!-- Actions droite -->
        <div class="flex items-center gap-3">
          <router-link to="/login"
                       class="hidden sm:block text-[10px] font-bold uppercase tracking-[0.25em]
                              text-neutral-400 hover:text-neutral-900 transition-colors">
            Connexion
          </router-link>
          <router-link to="/register"
                       class="px-5 py-2.5 text-[10px] font-bold uppercase tracking-[0.2em] rounded-xl
                              bg-neutral-900 text-white hover:bg-primary-700 transition-all">
            Commencer
          </router-link>

          <!-- Burger mobile -->
          <button class="md:hidden p-2 rounded-lg text-neutral-700 transition-colors"
                  @click="menuOpen = !menuOpen"
                  :aria-expanded="menuOpen"
                  aria-label="Ouvrir le menu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!menuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-else           stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

      </div>

      <!-- Menu mobile déroulant -->
      <Transition name="menu">
        <div v-if="menuOpen"
             class="md:hidden bg-white border-t border-primary-100 px-4 pb-4 pt-2 space-y-1 shadow-lg">
          <a v-for="[href, label] in [['#concept','Comment ça marche'],['#modeles','Designs'],['#avis','Avis']]"
             :key="href" :href="href"
             class="block py-3 text-[11px] font-bold uppercase tracking-[0.25em] text-neutral-600
                    border-b border-neutral-50 hover:text-primary-600 transition-colors"
             @click="menuOpen = false">
            {{ label }}
          </a>
          <div class="pt-3 flex flex-col gap-2">
            <router-link to="/login"   class="py-3 text-center text-[11px] font-bold uppercase tracking-[0.25em] text-neutral-500 hover:text-neutral-900 transition-colors" @click="menuOpen = false">Connexion</router-link>
            <router-link to="/register" class="py-3 bg-neutral-900 text-white text-center text-[11px] font-bold uppercase tracking-[0.25em] rounded-xl hover:bg-primary-700 transition-all" @click="menuOpen = false">Commencer</router-link>
          </div>
        </div>
      </Transition>
    </nav>

    <!-- ─── HERO ─────────────────────────────────────────────────────────────── -->
    <section id="hero-section"
             class="relative min-h-screen flex items-center overflow-hidden bg-[#FAF7F2]">

      <!-- Image de fond lumineuse avec voile blanc -->
      <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=60&w=1800"
           class="absolute inset-0 w-full h-full object-cover opacity-50"
           alt="" aria-hidden="true" loading="eager" fetchpriority="high" />
      <div class="absolute inset-0 bg-white/65" aria-hidden="true" />

      <!-- Lumières chaudes ambiantes -->
      <div class="absolute top-1/4 right-1/3 w-[500px] h-[500px] bg-primary-100/60 rounded-full blur-[140px] pointer-events-none" aria-hidden="true"/>
      <div class="absolute bottom-1/4 left-1/4 w-[400px] h-[400px] bg-amber-50/80 rounded-full blur-[120px] pointer-events-none" aria-hidden="true"/>

      <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20 w-full">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          <!-- Texte -->
          <div class="hero-text">
            <span class="inline-flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.5em] text-primary-600 mb-8">
              <span class="w-8 h-px bg-primary-400" aria-hidden="true"/>
              L'invitation digitale de votre mariage
            </span>

            <h2 class="font-serif italic text-[#2D2A26] leading-[1.25] md:leading-[1.05] mb-6">
              <span class="block text-5xl md:text-6xl xl:text-[72px]">Votre mariage,</span>
              <span class="block text-5xl md:text-6xl xl:text-[72px] mt-3 md:mt-1">
                votre&nbsp;<span class="inline-block overflow-hidden h-[1.1em] align-bottom">
                  <Transition name="word">
                    <span class="block text-primary-600" :key="heroWordIndex">{{ heroWords[heroWordIndex] }}.</span>
                  </Transition>
                </span>
              </span>
            </h2>

            <p class="text-[#2D2A26]/50 text-base font-light mb-10 max-w-sm">
              L'invitation que vos invités n'oublieront pas.
            </p>

            <div class="flex flex-col sm:flex-row gap-3">
              <button @click="handleCta"
                      class="px-8 py-4 bg-[#2D2A26] text-white rounded-xl text-[11px] font-bold uppercase tracking-[0.3em]
                             hover:bg-[#1A1816] transition-all shadow-xl shadow-neutral-900/10
                             transform hover:-translate-y-0.5 active:scale-95">
                Créer mon invitation
              </button>
              <a href="#modeles"
                 class="px-8 py-4 bg-white border border-neutral-200 text-[#2D2A26]/70 rounded-xl text-[11px]
                        font-bold uppercase tracking-[0.3em] hover:bg-neutral-50 transition-all text-center">
                Voir les designs
              </a>
            </div>

            <p class="mt-6 text-[10px] font-bold uppercase tracking-[0.25em] text-[#2D2A26]/25">
              Sans engagement · 5 minutes pour créer
            </p>
          </div>

          <!-- Mockup carte portrait -->
          <div class="hidden lg:flex items-center justify-center hero-image" aria-hidden="true">
            <div class="relative w-[280px]">
              <div class="aspect-[3/4] rounded-3xl overflow-hidden shadow-2xl ring-1 ring-neutral-200">
                <img src="https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800"
                     class="w-full h-full object-cover"
                     alt="Aperçu template Riviera Blanche" />
              </div>
              <div class="absolute -bottom-5 -left-10 bg-white rounded-2xl shadow-xl px-5 py-4 ring-1 ring-primary-100">
                <p class="text-[9px] font-bold uppercase tracking-widest text-primary-500 mb-1">RSVP reçus</p>
                <p class="text-2xl font-serif italic text-neutral-900">48 / 60</p>
              </div>
              <div class="absolute -top-5 -right-10 bg-white rounded-2xl shadow-xl px-5 py-4 ring-1 ring-primary-100">
                <div class="flex gap-0.5 mb-1" aria-label="Note 4.9 sur 5">
                  <span v-for="i in 5" :key="i" class="text-primary-400 text-sm" aria-hidden="true">★</span>
                </div>
                <p class="text-[9px] font-bold uppercase tracking-widest text-neutral-400">4.9 · 247 avis</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ─── COMMENT ÇA MARCHE ─────────────────────────────────────────────────── -->
    <section id="concept" class="py-24 bg-primary-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">

        <div data-section="steps-header"
             class="text-center mb-16 transition-all duration-700"
             :class="isVisible('steps-header') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 block mb-4">
            Comment ça marche
          </span>
          <h2 class="text-4xl md:text-5xl font-serif italic text-neutral-900">
            Simple. Élégant. Inoubliable.
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6" data-section="steps">
          <div v-for="(step, i) in steps" :key="step.number"
               class="bg-white rounded-3xl p-8 shadow-sm ring-1 ring-primary-100 transition-all duration-700"
               :class="isVisible('steps') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
               :style="{ transitionDelay: `${i * 120}ms` }">
            <span class="font-serif italic text-5xl text-primary-200 block mb-4" aria-hidden="true">{{ step.number }}</span>
            <h3 class="font-serif italic text-neutral-900 text-xl mb-3">{{ step.title }}</h3>
            <p class="text-neutral-400 text-sm font-light leading-relaxed">{{ step.description }}</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ─── TEMPLATES (vraies previews) ──────────────────────────────────────── -->
    <section id="modeles" class="py-24 bg-white overflow-hidden">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

        <div data-section="tpl-header"
             class="flex flex-col sm:flex-row sm:items-end justify-between gap-6 mb-14 transition-all duration-700"
             :class="isVisible('tpl-header') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 block mb-3">
              Collection 2026 · 14 designs exclusifs
            </span>
            <h2 class="text-4xl md:text-5xl font-serif italic text-neutral-900">
              Des designs qui vous ressemblent.
            </h2>
          </div>
          <router-link to="/register"
                       class="group inline-flex items-center gap-2 text-[11px] font-bold uppercase
                              tracking-[0.25em] text-primary-600 hover:text-primary-800 transition-colors shrink-0">
            Tout explorer
            <svg class="w-4 h-4 transition-transform group-hover:translate-x-1"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </router-link>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6" data-section="templates">
          <div v-for="(tpl, i) in LANDING_TEMPLATES" :key="tpl.id"
               class="group cursor-pointer transition-all duration-700"
               :class="isVisible('templates') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'"
               :style="{ transitionDelay: `${i * 80}ms` }"
               @click="router.push(`/demo/${tpl.id}`)">

            <div class="relative aspect-[3/4] overflow-hidden rounded-2xl bg-neutral-100 shadow-md
                        group-hover:shadow-xl transition-shadow duration-500">
              <img :src="tpl.image || `/previews/${tpl.id}.webp`" :alt="tpl.name" loading="lazy"
                   class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                   @error="$event.target.src='https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600'" />

              <div class="absolute inset-0 flex items-center justify-center
                          bg-black/0 group-hover:bg-black/25 transition-colors duration-500">
                <span class="opacity-0 group-hover:opacity-100 transition-all duration-300 delay-75
                             translate-y-2 group-hover:translate-y-0
                             px-5 py-3 bg-white text-neutral-900 text-[10px] font-bold
                             uppercase tracking-[0.25em] rounded-xl shadow-lg">
                  Voir le template
                </span>
              </div>

              <div v-if="tpl.isPremium" class="absolute top-3 right-3 z-10">
                <span class="text-[9px] font-bold uppercase tracking-widest px-3 py-1.5
                             rounded-full bg-primary-500 text-white shadow-sm">Premium</span>
              </div>
            </div>

            <div class="mt-3 px-1">
              <h3 class="font-serif italic text-neutral-900 text-base">{{ tpl.name }}</h3>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ─── FORFAITS ──────────────────────────────────────────────────────────── -->
    <section id="forfaits" class="py-24 bg-white">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">

        <!-- Header -->
        <div class="text-center mb-14">
          <span class="inline-flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-5">
            <span class="w-8 h-px bg-primary-300" aria-hidden="true"/>
            Tarifs
            <span class="w-8 h-px bg-primary-300" aria-hidden="true"/>
          </span>
          <h2 class="text-3xl md:text-4xl font-serif italic text-neutral-900 mb-3">Deux forfaits, un seul paiement</h2>
          <p class="text-neutral-400 font-light max-w-md mx-auto">
            Pas d'abonnement. Vous payez une fois, votre invitation reste en ligne jusqu'au grand jour.
          </p>
        </div>

        <!-- Cards — prix compact, survol (ou focus clavier) révèle les détails.
             Sur mobile (pas de survol) les détails restent toujours visibles. -->
        <div data-section="forfaits"
             class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 max-w-3xl mx-auto items-start transition-all duration-700"
             :class="isVisible('forfaits') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'">
          <div v-for="plan in plans" :key="plan.id" tabindex="0"
               class="group relative rounded-3xl bg-white outline-none transition-all duration-500
                      lg:hover:-translate-y-1 focus-visible:ring-2 focus-visible:ring-primary-300"
               :class="plan.highlight
                 ? 'border-2 border-primary-400 shadow-xl shadow-primary-200/40'
                 : 'border border-neutral-200 shadow-sm hover:shadow-lg'">

            <span v-if="plan.highlight"
                  class="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-primary-500
                         text-white text-[9px] font-bold uppercase tracking-[0.2em] shadow-sm z-10">
              Recommandé
            </span>

            <!-- Face : prix (toujours visible) -->
            <div class="px-8 pt-9 pb-7 text-center rounded-3xl transition-colors duration-500
                        lg:group-hover:bg-primary-50/70 lg:group-focus-within:bg-primary-50/70">
              <p class="text-[10px] font-bold uppercase tracking-[0.35em] mb-4"
                 :class="plan.highlight ? 'text-primary-600' : 'text-neutral-400'">{{ plan.name }}</p>
              <div class="flex items-baseline justify-center gap-1">
                <span class="font-serif text-6xl text-neutral-900 leading-none">{{ plan.price }}</span>
                <span class="text-2xl text-neutral-400">€</span>
              </div>
              <p class="mt-2 text-[10px] uppercase tracking-[0.25em] text-neutral-400">paiement unique</p>
              <p class="mt-4 text-sm text-neutral-500 font-light">{{ plan.tagline }}</p>

              <!-- Indice de survol (desktop, masqué quand déplié) -->
              <span class="hidden lg:flex items-center justify-center gap-1.5 mt-5 text-[9px] font-bold uppercase tracking-[0.25em] text-neutral-300
                           transition-opacity duration-300 lg:group-hover:opacity-0 lg:group-focus-within:opacity-0">
                Survolez pour les détails
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>
                </svg>
              </span>
            </div>

            <!-- Détails révélés -->
            <div class="overflow-hidden transition-all duration-500 ease-out
                        max-h-[640px] opacity-100
                        lg:max-h-0 lg:opacity-0
                        lg:group-hover:max-h-[640px] lg:group-hover:opacity-100
                        lg:group-focus-within:max-h-[640px] lg:group-focus-within:opacity-100">
              <div class="px-8 pb-8 pt-1">
                <div class="h-px bg-neutral-100 mb-6"></div>
                <ul class="space-y-3 mb-7">
                  <li v-for="feat in plan.features" :key="feat" class="flex items-start gap-3 text-sm text-neutral-700">
                    <svg class="w-4 h-4 mt-0.5 shrink-0" :class="plan.highlight ? 'text-primary-500' : 'text-neutral-400'"
                         fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                    </svg>
                    <span class="font-light">{{ feat }}</span>
                  </li>
                </ul>
                <button @click="handleCta"
                        class="w-full py-4 rounded-2xl text-[10px] font-bold uppercase tracking-[0.25em] transition-all active:scale-95"
                        :class="plan.highlight
                          ? 'bg-neutral-900 text-white hover:bg-primary-700 shadow-lg shadow-neutral-900/10'
                          : 'border border-neutral-300 text-neutral-700 hover:border-neutral-900 hover:text-neutral-900'">
                  Choisir {{ plan.name }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <p class="text-center mt-8 text-[10px] font-bold uppercase tracking-[0.25em] text-neutral-300">
          Passage de Classic à Premium possible à tout moment
        </p>
      </div>
    </section>

    <!-- ─── CTA FINAL ─────────────────────────────────────────────────────────── -->
    <section class="py-24 bg-primary-50 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px]
                    bg-primary-100 rounded-full blur-[120px] opacity-50"/>
      </div>

      <div data-section="cta"
           class="max-w-xl mx-auto px-4 sm:px-6 text-center relative z-10 transition-all duration-700"
           :class="isVisible('cta') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">

        <span class="inline-flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-8">
          <span class="w-8 h-px bg-primary-300" aria-hidden="true"/>
          Commencez aujourd'hui
          <span class="w-8 h-px bg-primary-300" aria-hidden="true"/>
        </span>

        <h2 class="text-4xl md:text-5xl font-serif italic text-neutral-900 mb-6 leading-tight">
          Votre plus beau jour<br>mérite la perfection.
        </h2>
        <p class="text-neutral-400 font-light mb-10">
          Rejoignez des milliers de couples qui ont choisi l'élégance digitale.
        </p>

        <button @click="handleCta"
                class="px-10 py-5 bg-neutral-900 text-white rounded-2xl text-[11px] font-bold uppercase
                       tracking-[0.3em] hover:bg-primary-700 transition-all shadow-xl shadow-neutral-900/10
                       transform hover:-translate-y-1 active:scale-95">
          Créer mon invitation
        </button>

        <p class="mt-6 text-[10px] font-bold uppercase tracking-[0.25em] text-neutral-300">
          Sans engagement · Configuration en 5 minutes
        </p>
      </div>
    </section>

    <!-- ─── SOCIAL PROOF (avis en fin de page) ──────────────────────────────────── -->
    <SocialProofBanner id="avis" />

    <!-- ─── FOOTER ────────────────────────────────────────────────────────────── -->
    <footer class="bg-neutral-900 pt-16 pb-10 border-t border-white/5">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

        <div class="flex flex-col md:flex-row justify-between items-start gap-12 mb-12 pb-12 border-b border-white/[0.07]">
          <div>
            <h2 class="text-xl font-serif italic text-white mb-2">Saas Wedding</h2>
            <p class="text-neutral-500 text-sm font-light max-w-xs leading-relaxed">
              Le compagnon digital de votre plus belle journée.
            </p>
          </div>
          <div class="flex flex-wrap gap-12">
            <div>
              <p class="text-[9px] font-bold uppercase tracking-widest text-neutral-600 mb-4">Navigation</p>
              <div class="flex flex-col gap-2.5">
                <a v-for="[href, label] in [['#modeles','Designs'],['#concept','Comment ça marche'],['#forfaits','Tarifs'],['#avis','Avis']]"
                   :key="href" :href="href"
                   class="text-sm text-neutral-500 hover:text-white transition-colors">{{ label }}</a>
              </div>
            </div>
            <div>
              <p class="text-[9px] font-bold uppercase tracking-widest text-neutral-600 mb-4">Légal</p>
              <div class="flex flex-col gap-2.5">
                <a v-for="label in ['Mentions légales','Confidentialité','Contact']" :key="label"
                   href="#" class="text-sm text-neutral-500 hover:text-white transition-colors">{{ label }}</a>
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col md:flex-row justify-between items-center gap-4
                    text-[10px] font-bold uppercase tracking-[0.2em] text-neutral-700">
          <p>© 2026 Saas Wedding — Fait avec amour pour les futurs mariés.</p>
          <p>18 designs · 2 forfaits · 1 grand jour</p>
        </div>

      </div>
    </footer>

  </div>
</template>

<style scoped>
/* Hero entrance */
.hero-text  { animation: fadeUp 0.9s 0.15s both cubic-bezier(0.16, 1, 0.3, 1); }
.hero-image { animation: fadeUp 0.9s 0.35s both cubic-bezier(0.16, 1, 0.3, 1); }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Cycling word */
.word-enter-active { animation: wordIn  0.5s cubic-bezier(0.16, 1, 0.3, 1) both; }
.word-leave-active { animation: wordOut 0.3s cubic-bezier(0.7, 0, 1, 0.5)  both; }
@keyframes wordIn  { from { transform: translateY(110%); opacity: 0; } to { transform: translateY(0);    opacity: 1; } }
@keyframes wordOut { from { transform: translateY(0);    opacity: 1; } to { transform: translateY(-110%); opacity: 0; } }

/* Menu mobile */
.menu-enter-active, .menu-leave-active { transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
.menu-enter-from, .menu-leave-to       { opacity: 0; transform: translateY(-8px); }
</style>
