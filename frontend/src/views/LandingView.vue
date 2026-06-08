<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../service/api';

const router = useRouter();
const auth = useAuthStore();

const scrolled = ref(false);
const handleScroll = () => { scrolled.value = window.scrollY > 60; };

const handlePlanSelection = async (planId) => {
  if (auth.user) {
    try {
      const res = await api.post('/payments/create-checkout-session', { plan_name: planId });
      if (res.data.checkout_url) { window.location.href = res.data.checkout_url; return; }
    } catch (e) { console.error(e); }
    router.push('/dashboard');
  } else {
    router.push({ path: '/register', query: { plan: planId } });
  }
};

// Animated hero word cycling
const heroWordIndex = ref(0);
const heroWords = ['élégance', 'passion', 'émotion'];
let wordTimer = null;

// Scroll reveal
const visible = ref(new Set());
let observer = null;
const isVisible = (s) => visible.value.has(s);


const templates = [
  {
    id: 'velvet-noir',
    name: 'Velvet Noir',
    subtitle: 'Luxe Nocturne',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1549416878-b5a76567bec9?auto=format&fit=crop&q=80&w=800',
    description: 'Rideaux qui s\'ouvrent, flammes CSS, particules lumineuses ascendantes. L\'expérience la plus envoûtante.',
  },
  {
    id: 'gatsby',
    name: 'Art Déco',
    subtitle: 'Grande Gatsby',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=800',
    description: 'Lignes géométriques dorées, symétrie absolue. Les années folles dans toute leur splendeur.',
  },
  {
    id: 'celeste',
    name: 'Céleste',
    subtitle: 'Nuit Étoilée',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&q=80&w=800',
    description: 'Constellations animées, parallaxe profond. Une invitation venue des étoiles.',
  },
  {
    id: 'riviera-blanche',
    name: 'Riviera Blanche',
    subtitle: 'Éditorial Côtier',
    tag: 'Classic',
    image: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800',
    description: 'Blanc chaud, bleu marine profond, minimalisme végétal. L\'élégance à la française.',
  },
  {
    id: 'wabi-sabi',
    name: 'Wabi-Sabi',
    subtitle: 'Jardin Japonais',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?auto=format&fit=crop&q=80&w=800',
    description: 'Traits d\'encre SVG animés, pétales tombants, papier ivoire texturé. La sérénité zen.',
  },
  {
    id: 'noir-eternel',
    name: 'Noir Éternel',
    subtitle: 'Élégance Intemporelle',
    tag: 'Classic',
    image: 'https://images.unsplash.com/photo-1606216794079-73d0b3eb5d8c?auto=format&fit=crop&q=80&w=800',
    description: 'Noir profond, typographie serif or, monogramme raffiné. Le summum du chic intemporel.',
  },
];

const marqueeItems = [
  'Velvet Noir', 'Art Déco — Grande Gatsby', 'Céleste — Nuit Étoilée',
  'Wabi-Sabi — Jardin Japonais', 'Riviera Blanche', 'Jardin Céleste',
  'Empire Abstrait', 'Cinématique 35mm', 'Noir Éternel',
  'Riviera Anni 70', 'Maison Haute Couture', 'Jardin Japonais',
];

const steps = [
  {
    number: '01',
    title: 'Choisissez votre design',
    description: 'Parcourez 18 templates exclusifs, des plus classiques aux plus avant-gardistes.',
  },
  {
    number: '02',
    title: 'Personnalisez chaque détail',
    description: 'Textes, couleurs, photos, musique. Un éditeur visuel intuitif pour un résultat sur-mesure.',
  },
  {
    number: '03',
    title: 'Partagez & organisez',
    description: 'Un lien unique pour vos invités. Collectez les RSVP, gérez les tables, vivez pleinement.',
  },
];

const features = [
  {
    icon: '✦',
    title: 'Édition Visuelle',
    description: 'Modifiez textes, couleurs et photos directement depuis un éditeur en temps réel, sans aucune compétence technique.',
  },
  {
    icon: '◎',
    title: 'RSVP Intelligent',
    description: 'Collectez les réponses en temps réel. Accompagnants, régimes alimentaires, messages — tout centralisé.',
  },
  {
    icon: '▦',
    title: 'Plan de Table',
    description: 'Placez vos invités par glisser-déposer. Exportez votre plan en CSV pour le traiteur le jour J.',
  },
];

const plans = [
  {
    id: 'classic',
    name: 'Classic',
    price: '29',
    description: 'L\'essentiel pour une invitation élégante.',
    features: [
      { text: 'Templates Classic inclus', ok: true },
      { text: 'RSVP illimité', ok: true },
      { text: 'Gestion des tables', ok: true },
      { text: 'Lien de partage unique', ok: true },
      { text: 'Templates Premium (accès verrouillé)', ok: false },
      { text: 'Import / Export CSV invités', ok: false },
      { text: 'Upload musique MP3', ok: false },
    ],
    cta: 'Commencer',
    popular: false,
  },
  {
    id: 'premium',
    name: 'Premium',
    price: '79',
    description: 'Une expérience sur-mesure pour votre grand jour.',
    features: [
      { text: 'Tous les templates Premium (13 designs)', ok: true },
      { text: 'RSVP illimité', ok: true },
      { text: 'Gestion des tables avancée', ok: true },
      { text: 'Lien personnalisé', ok: true },
      { text: 'Import / Export CSV invités', ok: true },
      { text: 'Upload musique MP3', ok: true },
      { text: 'Accès prioritaire aux nouveaux designs', ok: true },
    ],
    cta: 'Devenir Premium',
    popular: true,
  },
];

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true });

  wordTimer = setInterval(() => {
    heroWordIndex.value = (heroWordIndex.value + 1) % heroWords.length;
  }, 2800);

  observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const s = e.target.dataset.section;
        visible.value = new Set([...visible.value, s]);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('[data-section]').forEach(el => observer.observe(el));
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  if (wordTimer) clearInterval(wordTimer);
  if (observer) observer.disconnect();
});
</script>

<template>
  <div class="min-h-screen bg-white font-sans selection:bg-primary-100 selection:text-primary-900">

    <!-- ─── NAV ─────────────────────────────────────────────────────────────── -->
    <nav class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
         :class="scrolled
           ? 'bg-white/95 backdrop-blur-xl border-b border-neutral-100 shadow-sm'
           : 'bg-transparent border-b border-transparent'">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 h-20 flex items-center justify-between">
        <h1 class="text-xl font-serif italic transition-colors duration-500"
            :class="scrolled ? 'text-neutral-900' : 'text-white'">
          Saas Wedding
        </h1>

        <div class="hidden md:flex items-center gap-10">
          <a v-for="link in [['#modeles','Modèles'],['#concept','Concept'],['#tarifs','Tarifs']]"
             :key="link[0]" :href="link[0]"
             class="text-[10px] font-bold uppercase tracking-[0.25em] transition-colors duration-500 hover:opacity-100"
             :class="scrolled ? 'text-neutral-400 hover:text-neutral-900' : 'text-white/50 hover:text-white'">
            {{ link[1] }}
          </a>
        </div>

        <div class="flex items-center gap-4">
          <router-link to="/login"
                       class="text-[10px] font-bold uppercase tracking-[0.25em] transition-colors duration-500"
                       :class="scrolled ? 'text-neutral-400 hover:text-neutral-900' : 'text-white/50 hover:text-white'">
            Connexion
          </router-link>
          <router-link to="/register"
                       class="px-6 py-3 text-[10px] font-bold uppercase tracking-[0.25em] rounded-xl transition-all duration-300"
                       :class="scrolled
                         ? 'bg-neutral-900 text-white hover:bg-primary-900'
                         : 'bg-white/10 border border-white/20 text-white hover:bg-white/20 backdrop-blur-sm'">
            Créer mon invitation
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ─── HERO ──────────────────────────────────────────────────────────────── -->
    <section class="relative min-h-screen bg-[#0C0906] flex flex-col justify-end overflow-hidden">
      <!-- Background image -->
      <div class="absolute inset-0">
        <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=50&w=2000"
             class="w-full h-full object-cover opacity-[0.18]" alt="" aria-hidden="true" />
        <div class="absolute inset-0 bg-gradient-to-b from-[#0C0906]/40 via-[#0C0906]/70 to-[#0C0906]" />
      </div>

      <!-- Ambient orbs -->
      <div class="absolute top-1/3 right-1/4 w-[500px] h-[500px] bg-primary-500/8 rounded-full blur-[120px] orb-pulse pointer-events-none" />
      <div class="absolute bottom-1/3 left-1/4 w-[400px] h-[400px] bg-primary-700/6 rounded-full blur-[100px] orb-pulse-slow pointer-events-none" />

      <!-- Content -->
      <div class="relative z-10 max-w-7xl mx-auto px-6 lg:px-8 pb-28 pt-40">
        <!-- Eyebrow -->
        <div class="hero-line-1 mb-10">
          <span class="inline-flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.5em] text-primary-400">
            <span class="w-10 h-px bg-primary-400/60" />
            L'invitation digitale nouvelle génération
            <span class="w-10 h-px bg-primary-400/60" />
          </span>
        </div>

        <!-- Main title -->
        <h2 class="hero-line-2 font-serif italic text-white leading-[1.02] mb-14">
          <span class="block text-5xl md:text-7xl lg:text-8xl xl:text-[96px]">Votre mariage,</span>
          <span class="block text-5xl md:text-7xl lg:text-8xl xl:text-[96px] mt-1">
            votre&nbsp;<span class="inline-block overflow-hidden h-[1.1em] align-bottom w-fit">
              <Transition name="word">
                <span class="block text-primary-400" :key="heroWordIndex">
                  {{ heroWords[heroWordIndex] }}.
                </span>
              </Transition>
            </span>
          </span>
        </h2>

        <!-- Bottom row: desc + CTAs -->
        <div class="hero-line-3 flex flex-col lg:flex-row items-start lg:items-end gap-12">
          <p class="text-base md:text-lg text-white/35 font-light leading-relaxed max-w-md">
            Créez une invitation digitale sublime en quelques minutes. Gérez vos invités,
            collectez les RSVP et organisez votre plan de table en toute sérénité.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 lg:ml-auto shrink-0">
            <button @click="handlePlanSelection('classic')"
                    class="px-10 py-5 bg-primary-500 text-white rounded-2xl text-[11px] font-bold uppercase tracking-[0.3em] hover:bg-primary-400 transition-all shadow-2xl shadow-primary-900/40 transform hover:-translate-y-1 active:scale-95">
              Créer mon invitation
            </button>
            <a href="#modeles"
               class="px-10 py-5 bg-white/6 border border-white/10 text-white/75 rounded-2xl text-[11px] font-bold uppercase tracking-[0.3em] hover:bg-white/12 transition-all backdrop-blur-sm text-center transform hover:-translate-y-1">
              Voir les designs
            </a>
          </div>
        </div>

        <!-- Scroll hint -->
        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 scroll-hint">
          <span class="text-[9px] font-bold uppercase tracking-[0.4em] text-white/20">Découvrir</span>
          <div class="w-px h-10 bg-gradient-to-b from-white/20 to-transparent" />
        </div>
      </div>
    </section>

    <!-- ─── MARQUEE ────────────────────────────────────────────────────────────── -->
    <section class="py-5 bg-primary-500 overflow-hidden select-none">
      <div class="flex">
        <div class="marquee-track flex gap-12 items-center whitespace-nowrap pr-12 shrink-0">
          <span v-for="(item, i) in [...marqueeItems, ...marqueeItems, ...marqueeItems]"
                :key="i"
                class="text-[10px] font-bold uppercase tracking-[0.45em] text-primary-900 shrink-0 flex items-center gap-4">
            <span class="w-1 h-1 rounded-full bg-primary-900/25 inline-block" />
            {{ item }}
          </span>
        </div>
      </div>
    </section>

    <!-- ─── TEMPLATES ─────────────────────────────────────────────────────────── -->
    <section id="modeles" class="py-32 bg-neutral-50">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">

        <!-- Header -->
        <div data-section="tpl-header"
             class="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-20 transition-all duration-700"
             :class="isVisible('tpl-header') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 block mb-4">
              Collection 2026 · 18 designs exclusifs
            </span>
            <h2 class="text-4xl md:text-6xl font-serif italic text-neutral-900 leading-tight">
              Des designs<br>qui vous ressemblent.
            </h2>
          </div>
          <router-link to="/register"
                       class="group flex items-center gap-3 text-[11px] font-bold uppercase tracking-[0.25em] text-primary-600 hover:text-primary-800 transition-colors shrink-0">
            Explorer toute la collection
            <svg class="w-4 h-4 transition-transform group-hover:translate-x-1"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </router-link>
        </div>

        <!-- Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8" data-section="templates">
          <div v-for="(tpl, i) in templates" :key="tpl.id"
               class="group cursor-pointer transition-all duration-700"
               :class="isVisible('templates') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-14'"
               :style="{ transitionDelay: `${i * 90}ms` }"
               @click="router.push('/register')">

            <!-- Card -->
            <div class="relative aspect-[4/5] overflow-hidden rounded-3xl shadow-2xl bg-neutral-200">
              <img :src="tpl.image" :alt="tpl.name"
                   class="w-full h-full object-cover transition-transform duration-[800ms] group-hover:scale-110" />

              <!-- Gradient overlay (always present, darkens on hover) -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-transparent
                          opacity-70 group-hover:opacity-95 transition-opacity duration-500" />

              <!-- Tag -->
              <div class="absolute top-5 right-5">
                <span v-if="tpl.tag === 'Premium'"
                      class="flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-widest
                             px-3 py-1.5 rounded-full bg-primary-500 text-white shadow-lg shadow-primary-900/30">
                  <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Premium
                </span>
                <span v-else
                      class="text-[9px] font-bold uppercase tracking-widest px-3 py-1.5 rounded-full
                             bg-white/15 text-white border border-white/25 backdrop-blur-sm">
                  Classic
                </span>
              </div>

              <!-- Premium blur overlay (visible only when not hovering) -->
              <div v-if="tpl.tag === 'Premium'"
                   class="absolute inset-0 flex items-center justify-center
                          opacity-0 group-hover:opacity-0 transition-opacity duration-300 pointer-events-none">
              </div>

              <!-- Bottom content -->
              <div class="absolute bottom-0 left-0 right-0 p-7">
                <p class="text-[10px] font-bold uppercase tracking-[0.35em] text-primary-400 mb-1.5">
                  {{ tpl.subtitle }}
                </p>
                <h3 class="text-2xl font-serif italic text-white leading-snug">{{ tpl.name }}</h3>

                <!-- Revealed on hover -->
                <div class="overflow-hidden transition-all duration-500 max-h-0 group-hover:max-h-24">
                  <p class="text-white/65 text-sm font-light leading-relaxed pt-3">
                    {{ tpl.description }}
                  </p>
                </div>

                <div class="overflow-hidden transition-all duration-500 max-h-0 group-hover:max-h-16">
                  <div class="pt-5">
                    <span v-if="tpl.tag === 'Premium'"
                          class="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.25em]
                                 px-5 py-3 bg-primary-500/20 border border-primary-400/40 text-primary-300 rounded-xl
                                 hover:bg-primary-500 hover:text-white hover:border-primary-500 transition-all">
                      <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      Accès Premium requis
                    </span>
                    <span v-else
                          class="inline-block text-[10px] font-bold uppercase tracking-[0.3em] px-5 py-3
                                 border border-white/30 text-white rounded-xl
                                 hover:bg-white hover:text-neutral-900 transition-all">
                      Choisir ce design
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Below card -->
            <div class="mt-4 px-1 flex items-center justify-between">
              <h4 class="font-serif italic text-neutral-900 text-lg">{{ tpl.name }}</h4>
              <span class="text-[9px] font-bold uppercase tracking-widest text-neutral-400">{{ tpl.tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── HOW IT WORKS ──────────────────────────────────────────────────────── -->
    <section id="concept" class="py-32 bg-[#0C0906] relative overflow-hidden">
      <!-- Decorative rings -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px]
                  border border-white/[0.04] rounded-full pointer-events-none" />
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[1000px]
                  border border-white/[0.02] rounded-full pointer-events-none" />

      <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">

        <!-- Section header -->
        <div data-section="steps-header"
             class="text-center mb-24 transition-all duration-700"
             :class="isVisible('steps-header') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-400 block mb-6">
            Comment ça marche
          </span>
          <h2 class="text-4xl md:text-6xl font-serif italic text-white leading-tight">
            Simple. Élégant. Inoubliable.
          </h2>
        </div>

        <!-- Steps -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 lg:gap-20 mb-24" data-section="steps">
          <div v-for="(step, i) in steps" :key="step.number"
               class="relative transition-all duration-700"
               :class="isVisible('steps') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'"
               :style="{ transitionDelay: `${i * 150}ms` }">
            <div v-if="i < 2"
                 class="hidden md:block absolute top-8 left-[calc(50%+40px)] right-[-20px] h-px
                        bg-gradient-to-r from-white/10 to-transparent" />

            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/8 flex items-center justify-center mb-8">
              <span class="font-serif italic text-primary-400 text-lg">{{ step.number }}</span>
            </div>
            <h3 class="text-xl font-serif italic text-white mb-4">{{ step.title }}</h3>
            <p class="text-white/35 font-light leading-relaxed text-sm">{{ step.description }}</p>
          </div>
        </div>

        <!-- Feature cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5" data-section="features">
          <div v-for="(feat, i) in features" :key="feat.title"
               class="p-8 rounded-2xl bg-white/[0.03] border border-white/6 hover:bg-white/6
                      hover:border-white/10 transition-all duration-400 group
                      transition-all duration-700"
               :class="isVisible('features') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'"
               :style="{ transitionDelay: `${i * 100}ms` }">
            <div class="text-2xl mb-5 text-primary-400 group-hover:scale-110 transition-transform duration-300 inline-block">
              {{ feat.icon }}
            </div>
            <h4 class="font-serif italic text-white text-lg mb-3">{{ feat.title }}</h4>
            <p class="text-white/35 text-sm leading-relaxed">{{ feat.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── PRICING ───────────────────────────────────────────────────────────── -->
    <section id="tarifs" class="py-32 bg-white">
      <div class="max-w-5xl mx-auto px-6 lg:px-8">

        <!-- Header -->
        <div data-section="pricing-header"
             class="text-center mb-20 transition-all duration-700"
             :class="isVisible('pricing-header') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
          <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 block mb-4">
            Investissement
          </span>
          <h2 class="text-4xl md:text-5xl font-serif italic text-neutral-900 leading-tight">
            Un prix juste pour<br>un jour unique.
          </h2>
        </div>

        <!-- Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8" data-section="pricing">
          <div v-for="(plan, i) in plans" :key="plan.id"
               class="relative rounded-3xl p-10 flex flex-col transition-all duration-700"
               :class="[
                 isVisible('pricing') ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10',
                 plan.popular
                   ? 'bg-neutral-900 shadow-2xl shadow-neutral-900/20'
                   : 'bg-neutral-50 border border-neutral-100'
               ]"
               :style="{ transitionDelay: `${i * 150}ms` }">

            <div v-if="plan.popular"
                 class="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary-500 text-white
                        text-[9px] font-bold uppercase tracking-widest px-5 py-2 rounded-full shadow-lg">
              Le choix des mariés
            </div>

            <div class="mb-8">
              <h3 class="text-xl font-serif italic mb-2"
                  :class="plan.popular ? 'text-white' : 'text-neutral-900'">
                Forfait {{ plan.name }}
              </h3>
              <p class="text-sm font-light"
                 :class="plan.popular ? 'text-white/45' : 'text-neutral-400'">
                {{ plan.description }}
              </p>
            </div>

            <div class="flex items-baseline mb-10">
              <span class="text-6xl font-serif italic"
                    :class="plan.popular ? 'text-primary-400' : 'text-neutral-900'">
                {{ plan.price }}€
              </span>
              <span class="ml-2 text-[10px] font-bold uppercase tracking-widest"
                    :class="plan.popular ? 'text-white/25' : 'text-neutral-400'">
                / mariage
              </span>
            </div>

            <ul class="space-y-4 mb-10 flex-grow">
              <li v-for="f in plan.features" :key="f.text" class="flex items-center gap-3 text-sm">
                <svg v-if="f.ok" class="w-4 h-4 shrink-0"
                     :class="plan.popular ? 'text-primary-400' : 'text-primary-500'"
                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else class="w-4 h-4 shrink-0 opacity-20"
                     :class="plan.popular ? 'text-white' : 'text-neutral-400'"
                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span :class="f.ok
                  ? (plan.popular ? 'text-white/80' : 'text-neutral-700')
                  : (plan.popular ? 'text-white/20' : 'text-neutral-300')">
                  {{ f.text }}
                </span>
              </li>
            </ul>

            <button @click="handlePlanSelection(plan.id)"
                    class="w-full py-4 rounded-xl text-[11px] font-bold uppercase tracking-[0.3em]
                           transition-all duration-300 transform hover:-translate-y-0.5 active:scale-95"
                    :class="plan.popular
                      ? 'bg-primary-500 text-white hover:bg-primary-400 shadow-xl shadow-primary-900/20'
                      : 'bg-neutral-900 text-white hover:bg-neutral-800'">
              {{ plan.cta }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── FINAL CTA ─────────────────────────────────────────────────────────── -->
    <section class="py-32 bg-neutral-50 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none overflow-hidden">
        <div class="absolute -top-1/2 left-1/2 -translate-x-1/2 w-[900px] h-[900px]
                    bg-primary-100 rounded-full blur-[120px] opacity-60" />
      </div>

      <div data-section="cta"
           class="max-w-3xl mx-auto px-6 text-center relative z-10 transition-all duration-1000"
           :class="isVisible('cta') ? 'opacity-100 scale-100' : 'opacity-0 scale-[0.97]'">
        <span class="inline-flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-10">
          <span class="w-10 h-px bg-primary-300" />
          Commencez aujourd'hui
          <span class="w-10 h-px bg-primary-300" />
        </span>

        <h2 class="text-4xl md:text-6xl font-serif italic text-neutral-900 mb-8 leading-tight">
          Votre plus beau jour<br>mérite la perfection.
        </h2>

        <p class="text-lg text-neutral-400 font-light mb-14 leading-relaxed">
          Rejoignez des milliers de couples qui ont choisi l'élégance digitale<br class="hidden md:block" />
          pour vivre leur grand jour sereinement.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register"
                       class="px-12 py-5 bg-neutral-900 text-white rounded-2xl text-[11px] font-bold uppercase
                              tracking-[0.3em] hover:bg-primary-900 transition-all shadow-2xl shadow-neutral-900/15
                              transform hover:-translate-y-1 active:scale-95">
            Créer mon invitation
          </router-link>
          <a href="#modeles"
             class="px-12 py-5 bg-white border border-neutral-200 text-neutral-900 rounded-2xl text-[11px]
                    font-bold uppercase tracking-[0.3em] hover:bg-neutral-50 transition-all shadow-xl
                    transform hover:-translate-y-1 text-center">
            Voir les designs
          </a>
        </div>

        <p class="mt-10 text-[10px] font-bold uppercase tracking-[0.25em] text-neutral-300">
          Sans engagement · Configuration en 5 minutes
        </p>
      </div>
    </section>

    <!-- ─── FOOTER ─────────────────────────────────────────────────────────────── -->
    <footer class="bg-neutral-900 pt-20 pb-12 border-t border-white/5">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-start gap-16 mb-16 pb-16 border-b border-white/5">
          <div>
            <h2 class="text-2xl font-serif italic text-white mb-3">Saas Wedding</h2>
            <p class="text-neutral-500 text-sm font-light max-w-xs leading-relaxed">
              Le compagnon digital de votre plus belle journée. Élégance, simplicité, émotion.
            </p>
          </div>

          <div class="flex flex-col sm:flex-row gap-14">
            <div>
              <p class="text-[9px] font-bold uppercase tracking-widest text-neutral-600 mb-5">Navigation</p>
              <div class="flex flex-col gap-3">
                <a v-for="link in [['#modeles','Nos Modèles'],['#concept','Comment ça marche'],['#tarifs','Tarifs']]"
                   :key="link[0]" :href="link[0]"
                   class="text-sm text-neutral-500 hover:text-white transition-colors">
                  {{ link[1] }}
                </a>
              </div>
            </div>
            <div>
              <p class="text-[9px] font-bold uppercase tracking-widest text-neutral-600 mb-5">Légal</p>
              <div class="flex flex-col gap-3">
                <a v-for="label in ['Mentions légales','Confidentialité','Contact']" :key="label"
                   href="#" class="text-sm text-neutral-500 hover:text-white transition-colors">
                  {{ label }}
                </a>
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
html { scroll-behavior: smooth; }

/* Hero text entrance */
.hero-line-1 { animation: fadeUp 0.9s 0.1s both cubic-bezier(0.16, 1, 0.3, 1); }
.hero-line-2 { animation: fadeUp 0.9s 0.3s both cubic-bezier(0.16, 1, 0.3, 1); }
.hero-line-3 { animation: fadeUp 0.9s 0.55s both cubic-bezier(0.16, 1, 0.3, 1); }
.scroll-hint { animation: fadeUp 0.9s 1.2s both cubic-bezier(0.16, 1, 0.3, 1); }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Animated word transition */
.word-enter-active { animation: wordIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both; }
.word-leave-active { animation: wordOut 0.3s cubic-bezier(0.7, 0, 1, 0.5) both; }

@keyframes wordIn {
  from { transform: translateY(110%); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}
@keyframes wordOut {
  from { transform: translateY(0); opacity: 1; }
  to   { transform: translateY(-110%); opacity: 0; }
}

/* Ambient orbs */
.orb-pulse       { animation: orbPulse 5s ease-in-out infinite; }
.orb-pulse-slow  { animation: orbPulse 7s ease-in-out 1.5s infinite; }

@keyframes orbPulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50%       { opacity: 0.7; transform: scale(1.08); }
}

/* Infinite marquee */
.marquee-track {
  animation: marqueeScroll 35s linear infinite;
}

@keyframes marqueeScroll {
  from { transform: translateX(0); }
  to   { transform: translateX(-33.333%); }
}

/* Scroll hint line bob */
@keyframes scrollBob {
  0%, 100% { transform: translateX(-50%) translateY(0); opacity: 1; }
  50%       { transform: translateX(-50%) translateY(6px); opacity: 0.4; }
}
</style>
