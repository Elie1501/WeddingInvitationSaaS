<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../service/api';

const router = useRouter();
const auth = useAuthStore();

const handlePlanSelection = async (planId) => {
  if (auth.user) {
    // Si déjà connecté, on tente de créer une session Stripe
    try {
      const response = await api.post('/payments/create-checkout-session', {
        plan_name: planId
      });
      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url;
        return;
      }
    } catch (err) {
      console.error("Erreur Stripe:", err);
    }
    router.push('/dashboard');
  } else {
    // Sinon on va à l'inscription avec le plan en paramètre
    router.push({ path: '/register', query: { plan: planId } });
  }
};

const templates = [
  {
    id: 'royal-gold',
    name: 'Royal Gold',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1510076857177-7470076d4098?auto=format&fit=crop&q=80&w=800',
    description: 'Luxe absolu, or et élégance royale.'
  },
  {
    id: 'bohemian-dream',
    name: 'Bohemian Dream',
    tag: 'Premium',
    image: 'https://images.unsplash.com/photo-1522673607200-164883eecd4c?auto=format&fit=crop&q=80&w=800',
    description: 'Nature, bohème et douceur de vivre.'
  },
  {
    id: 'modern-chic',
    name: 'Modern Chic',
    tag: 'Classic',
    image: 'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?auto=format&fit=crop&q=80&w=800',
    description: 'Minimalisme urbain et épuré.'
  }
];

const pricingPlans = [
  {
    id: 'classic',
    name: 'Forfait Classic',
    price: '29€',
    description: 'L\'essentiel pour une invitation élégante et rapide.',
    features: [
      'Templates standards inclus',
      'RSVP simple et illimité',
      'Gestion des tables basique',
      'Jusqu\'à 150 invités',
      'Lien de partage unique'
    ],
    cta: 'Choisir le forfait Classic',
    popular: false
  },
  {
    id: 'premium',
    name: 'Forfait Premium',
    price: '59€',
    description: 'Une personnalisation complète pour un mariage d\'exception.',
    features: [
      'Accès à TOUS les templates Premium',
      'Upload de votre propre musique (MP3)',
      'Import/Export des invités (CSV)',
      'Gestion complète des tables',
      'Jusqu\'à 1000 invités',
      'Support prioritaire'
    ],
    cta: 'Devenir Premium',
    popular: true
  }
];
</script>

<template>
  <div class="min-h-screen bg-white font-sans selection:bg-primary-100 selection:text-primary-900">
    <!-- Navigation -->
    <nav class="bg-white/90 backdrop-blur-xl sticky top-0 z-50 border-b border-neutral-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-20 items-center">
        <div class="flex items-center">
          <h1 class="text-2xl font-serif italic text-primary-900">Saas Wedding</h1>
        </div>
        <div class="hidden md:flex space-x-10 text-[11px] font-bold uppercase tracking-[0.2em] text-neutral-500">
          <a href="#concept" class="hover:text-primary-600 transition-colors">Concept</a>
          <a href="#modeles" class="hover:text-primary-600 transition-colors">Nos Modèles</a>
          <a href="#tarifs" class="hover:text-primary-600 transition-colors">Tarifs</a>
        </div>
        <div class="flex items-center space-x-6">
          <router-link to="/login" class="text-[11px] font-bold uppercase tracking-[0.2em] text-neutral-500 hover:text-primary-600 transition-colors">Connexion</router-link>
          <router-link to="/register" class="bg-neutral-900 text-white px-8 py-3.5 rounded-full text-[11px] font-bold uppercase tracking-[0.2em] hover:bg-primary-900 transition-all shadow-xl shadow-neutral-900/10">Créer mon invitation</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative pt-24 pb-40 overflow-hidden bg-neutral-50">
      <!-- Decor -->
      <div class="absolute top-0 right-0 w-1/2 h-full bg-primary-50/50 rounded-l-[5rem] -z-0 opacity-50"></div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 flex flex-col lg:flex-row items-center gap-20">
        <div class="lg:w-1/2 text-center lg:text-left">
          <span class="inline-block text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-6 bg-primary-50 px-4 py-2 rounded-full">L'invitation digitale nouvelle génération</span>
          <h2 class="text-5xl md:text-7xl text-neutral-900 mb-8 leading-[1.1] font-serif italic">
            Célébrez votre amour avec <span class="text-primary-600">élégance.</span>
          </h2>
          <p class="text-xl text-neutral-500 font-light max-w-xl mb-12 leading-relaxed">
            Créez une invitation digitale sublime en quelques minutes. Gérez vos invités, collectez les RSVP et organisez votre plan de table en toute sérénité.
          </p>
          <div class="flex flex-col sm:flex-row gap-6 justify-center lg:justify-start">
            <button @click="handlePlanSelection('classic')" class="px-10 py-5 bg-neutral-900 text-white rounded-2xl text-[12px] font-bold uppercase tracking-[0.3em] hover:bg-primary-900 transition-all shadow-2xl shadow-neutral-900/20 transform hover:-translate-y-1">Commencer gratuitement</button>
            <a href="#modeles" class="px-10 py-5 bg-white text-neutral-900 border border-neutral-200 rounded-2xl text-[12px] font-bold uppercase tracking-[0.3em] hover:bg-neutral-50 transition-all shadow-xl shadow-neutral-900/5 transform hover:-translate-y-1 text-center">Voir les modèles</a>
          </div>
        </div>
        
        <div class="lg:w-1/2 relative group">
          <div class="absolute inset-0 bg-primary-200 blur-[100px] opacity-20 group-hover:opacity-40 transition-opacity"></div>
          <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=1200" 
            class="relative z-10 rounded-[3rem] shadow-2xl border-8 border-white transform rotate-3 hover:rotate-0 transition-transform duration-700"
            alt="Wedding Template Preview">
        </div>
      </div>
    </section>

    <!-- Nos Modèles (Nouveau) -->
    <section id="modeles" class="py-32 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-end mb-20 gap-8">
          <div class="max-w-2xl">
            <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-4 block">Collection 2026</span>
            <h2 class="text-4xl md:text-5xl text-neutral-900 font-serif italic">Des designs qui racontent votre histoire</h2>
          </div>
          <router-link to="/register" class="text-[11px] font-bold uppercase tracking-[0.2em] text-primary-600 hover:text-primary-800 transition-all flex items-center">
            Voir toute la collection
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div v-for="tpl in templates" :key="tpl.id" class="group cursor-pointer">
            <div class="relative aspect-[4/5] rounded-[2.5rem] overflow-hidden shadow-2xl transition-all duration-700 group-hover:-translate-y-4">
              <img :src="tpl.image" :alt="tpl.name" class="w-full h-full object-cover transition-transform duration-[2s] group-hover:scale-110">
              <div class="absolute inset-0 bg-gradient-to-t from-neutral-900/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-10">
                <span class="text-[10px] font-bold uppercase tracking-[0.3em] text-white/70 mb-2">{{ tpl.tag }}</span>
                <h3 class="text-2xl text-white font-serif italic mb-4">{{ tpl.name }}</h3>
                <router-link to="/register" class="text-[10px] font-bold uppercase tracking-[0.2em] text-white border border-white/30 py-3 px-6 rounded-xl hover:bg-white hover:text-neutral-900 transition-all w-fit">Choisir ce style</router-link>
              </div>
              <div class="absolute top-6 right-6 bg-white/90 backdrop-blur-md px-4 py-2 rounded-full text-[9px] font-bold uppercase tracking-widest text-neutral-900 shadow-xl">
                {{ tpl.tag }}
              </div>
            </div>
            <div class="mt-8 text-center">
              <h3 class="text-xl text-neutral-900 font-serif italic mb-2">{{ tpl.name }}</h3>
              <p class="text-neutral-400 text-sm font-light tracking-wide">{{ tpl.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section (Concept) -->
    <section id="concept" class="py-32 bg-neutral-50 relative overflow-hidden">
      <!-- Abstract Decor -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] border border-primary-200/30 rounded-full -z-0"></div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center mb-24">
          <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-4 block">Organisation</span>
          <h2 class="text-4xl md:text-5xl text-neutral-900 font-serif italic">Tout pour un mariage serein</h2>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-16">
          <div class="group">
            <div class="w-20 h-20 bg-white rounded-3xl shadow-xl flex items-center justify-center mb-8 transform transition-transform group-hover:rotate-6 group-hover:scale-110 duration-500">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-neutral-900 font-serif italic">Édition Intuitive</h3>
            <p class="text-neutral-500 font-light leading-relaxed">Personnalisez chaque détail : textes, couleurs, musiques et photos. Créez plusieurs pages pour vos informations pratiques.</p>
          </div>
          
          <div class="group">
            <div class="w-20 h-20 bg-white rounded-3xl shadow-xl flex items-center justify-center mb-8 transform transition-transform group-hover:rotate-6 group-hover:scale-110 duration-500">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-neutral-900 font-serif italic">RSVP Intelligent</h3>
            <p class="text-neutral-500 font-light leading-relaxed">Collectez les réponses en temps réel. Gérez les accompagnants, les allergies et recevez les messages tendres de vos invités.</p>
          </div>
          
          <div class="group">
            <div class="w-20 h-20 bg-white rounded-3xl shadow-xl flex items-center justify-center mb-8 transform transition-transform group-hover:rotate-6 group-hover:scale-110 duration-500">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-neutral-900 font-serif italic">Plan de Table</h3>
            <p class="text-neutral-500 font-light leading-relaxed">Placez vos invités par simple glisser-déposer. Exportez votre plan final en CSV ou PDF pour le jour J.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Showcase Section (Mockups) -->
    <section class="py-32 bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row items-center gap-24">
          <div class="lg:w-1/2">
            <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-4 block">Expérience Invité</span>
            <h2 class="text-4xl md:text-5xl text-neutral-900 font-serif italic mb-8 leading-tight">L'élégance à portée de main.</h2>
            <p class="text-lg text-neutral-500 font-light mb-10 leading-relaxed">
              Vos invités reçoivent un lien personnalisé qui s'adapte parfaitement à leur smartphone. Une expérience fluide, sans application à télécharger, pour qu'ils puissent se concentrer sur l'essentiel : célébrer avec vous.
            </p>
            <ul class="space-y-6 mb-12">
              <li class="flex items-center text-neutral-900 font-serif italic text-lg">
                <span class="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center mr-4 text-primary-600 text-sm italic">01</span>
                Design Responsive & Fluide
              </li>
              <li class="flex items-center text-neutral-900 font-serif italic text-lg">
                <span class="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center mr-4 text-primary-600 text-sm italic">02</span>
                RSVP Instantané en 3 clics
              </li>
              <li class="flex items-center text-neutral-900 font-serif italic text-lg">
                <span class="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center mr-4 text-primary-600 text-sm italic">03</span>
                Itinéraire & Infos Pratiques
              </li>
            </ul>
            <router-link to="/register" class="inline-block text-[11px] font-bold uppercase tracking-[0.3em] text-primary-600 border-b-2 border-primary-200 pb-2 hover:border-primary-600 transition-all">
              Commencer ma personnalisation
            </router-link>
          </div>
          
          <div class="lg:w-1/2 relative">
            <!-- Mockups overlapping -->
            <div class="relative w-full aspect-square max-w-[500px] mx-auto">
              <img src="https://images.unsplash.com/photo-1544928147-79a2dbc1f389?auto=format&fit=crop&q=80&w=600" 
                class="absolute top-0 right-0 w-2/3 rounded-[3rem] shadow-2xl border-4 border-white z-20 transform rotate-6" 
                alt="Mobile Card Example 1">
              <img src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=600" 
                class="absolute bottom-0 left-0 w-2/3 rounded-[3rem] shadow-2xl border-4 border-white z-10 transform -rotate-12" 
                alt="Mobile Card Example 2">
              <div class="absolute inset-0 bg-primary-100 rounded-full blur-[100px] -z-10 opacity-30"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="tarifs" class="py-32 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-24">
          <span class="text-[10px] font-bold uppercase tracking-[0.5em] text-primary-500 mb-4 block">Investissement</span>
          <h2 class="text-4xl md:text-5xl text-neutral-900 font-serif italic">Des tarifs transparents</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-5xl mx-auto">
          <div v-for="plan in pricingPlans" :key="plan.name" 
            class="relative bg-white rounded-[3rem] p-12 md:p-16 border transition-all duration-500 flex flex-col h-full hover:shadow-[0_40px_80px_rgba(0,0,0,0.06)]"
            :class="plan.popular ? 'border-primary-200 shadow-2xl shadow-primary-900/5' : 'border-neutral-100'"
          >
            <div v-if="plan.popular" class="absolute top-0 right-16 -translate-y-1/2 bg-primary-600 text-white px-6 py-2 rounded-full text-[10px] font-bold uppercase tracking-widest">Le choix des mariés</div>
            
            <h3 class="text-2xl text-neutral-900 mb-4 font-serif italic">{{ plan.name }}</h3>
            <div class="flex items-baseline mb-8">
              <span class="text-5xl font-serif text-primary-900 italic">{{ plan.price }}</span>
              <span class="text-neutral-400 ml-3 text-[10px] font-bold uppercase tracking-widest">/ mariage</span>
            </div>
            <p class="text-neutral-500 font-light text-sm mb-12 leading-relaxed">{{ plan.description }}</p>
            
            <ul class="space-y-6 mb-16 flex-grow">
              <li v-for="feature in plan.features" :key="feature" class="flex items-start text-sm text-neutral-600 font-light">
                <svg class="w-5 h-5 text-primary-500 mr-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ feature }}
              </li>
            </ul>
            
            <button 
              @click="handlePlanSelection(plan.id)"
              class="w-full py-5 rounded-2xl text-center text-[12px] font-bold uppercase tracking-[0.3em] transition-all duration-500"
              :class="plan.popular ? 'bg-neutral-900 text-white hover:bg-primary-900 shadow-2xl shadow-neutral-900/20' : 'bg-neutral-50 text-neutral-900 hover:bg-neutral-100 border border-neutral-100'"
            >
              {{ plan.cta }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA Section -->
    <section class="py-32 bg-primary-900 relative overflow-hidden">
      <!-- Decor -->
      <div class="absolute top-0 left-0 w-full h-full opacity-10">
        <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-white rounded-full blur-[120px]"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary-400 rounded-full blur-[120px]"></div>
      </div>

      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <h2 class="text-4xl md:text-6xl text-white font-serif italic mb-8 leading-tight">
          Prêts à créer votre <span class="text-primary-300">moment inoubliable ?</span>
        </h2>
        <p class="text-xl text-primary-100/70 font-light mb-12 leading-relaxed">
          Rejoignez des milliers de couples qui ont choisi l'élégance et la simplicité pour leur grand jour. Commencez gratuitement aujourd'hui.
        </p>
        <div class="flex flex-col sm:flex-row gap-6 justify-center">
          <router-link to="/register" class="px-12 py-6 bg-white text-neutral-900 rounded-2xl text-[12px] font-bold uppercase tracking-[0.3em] hover:bg-primary-50 transition-all shadow-2xl transform hover:-translate-y-1">
            Créer mon invitation
          </router-link>
          <router-link to="/login" class="px-12 py-6 bg-transparent text-white border border-white/20 rounded-2xl text-[12px] font-bold uppercase tracking-[0.3em] hover:bg-white/10 transition-all transform hover:-translate-y-1">
            Me connecter
          </router-link>
        </div>
        <p class="mt-10 text-primary-200/50 text-[10px] font-bold uppercase tracking-[0.2em]">
          Sans engagement — Configuration en 5 minutes
        </p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-neutral-900 py-24 border-t border-white/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-12 mb-20 pb-20 border-b border-white/5">
            <div class="text-center md:text-left">
                <h2 class="text-3xl font-serif italic text-white mb-2">Saas Wedding</h2>
                <p class="text-neutral-500 font-light tracking-wide max-w-sm">Le compagnon digital de votre plus belle journée.</p>
            </div>
            <div class="flex gap-12 text-[10px] font-bold uppercase tracking-[0.3em] text-white/40">
                <a href="#concept" class="hover:text-white transition-colors">Concept</a>
                <a href="#modeles" class="hover:text-white transition-colors">Modèles</a>
                <a href="#tarifs" class="hover:text-white transition-colors">Tarifs</a>
            </div>
        </div>
        
        <div class="flex flex-col md:flex-row justify-between items-center gap-8 text-[10px] font-bold uppercase tracking-[0.2em] text-neutral-600">
            <p>© 2026 Saas Wedding — Fait avec amour pour les futurs mariés.</p>
            <div class="flex space-x-10">
                <a href="#" class="hover:text-white transition-colors">Mentions Légales</a>
                <a href="#" class="hover:text-white transition-colors">Confidentialité</a>
                <a href="#" class="hover:text-white transition-colors">Contact</a>
            </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
html {
  scroll-behavior: smooth;
}
</style>
