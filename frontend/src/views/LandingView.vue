<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const pricingPlans = [
  {
    name: 'Forfait Basique',
    price: '29€',
    description: 'L\'essentiel pour une invitation élégante et rapide.',
    features: [
      'Templates standards inclus',
      'Champs de configuration essentiels',
      'Musique de fond prédéfinie',
      'Jusqu\'à 50 invités',
      'Lien de partage unique'
    ],
    cta: 'Commencer en Basique',
    popular: false
  },
  {
    name: 'Forfait Avancé',
    price: '59€',
    description: 'Une personnalisation complète pour un mariage d\'exception.',
    features: [
      'Tous les templates premium',
      'Personnalisation étendue (couleurs, polices)',
      'Import/Export des invités (CSV)',
      'Gestion complète des tables',
      'Invités illimités'
    ],
    cta: 'Choisir l\'Avancé',
    popular: true
  }
];
</script>

<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <nav class="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-primary-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-20 items-center">
        <div class="flex items-center">
          <h1 class="text-2xl text-primary-800">Saas Wedding</h1>
        </div>
        <div class="hidden md:flex space-x-8 font-sans text-sm font-medium text-gray-600">
          <a href="#concept" class="hover:text-primary-600 transition-colors">Concept</a>
          <a href="#services" class="hover:text-primary-600 transition-colors">Services</a>
          <a href="#tarifs" class="hover:text-primary-600 transition-colors">Tarifs</a>
        </div>
        <div class="flex items-center space-x-4">
          <router-link to="/login" class="font-sans text-sm font-medium text-gray-600 hover:text-primary-600 transition-colors">Connexion</router-link>
          <router-link to="/register" class="bg-primary-600 text-white px-5 py-2.5 rounded-full font-sans text-sm font-medium hover:bg-primary-700 transition-all shadow-md shadow-primary-600/20">Créer ma carte</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative pt-20 pb-32 overflow-hidden">
      <div class="absolute top-0 right-0 -mr-20 -mt-20 w-1/2 h-1/2 bg-primary-100/50 rounded-full blur-3xl opacity-50"></div>
      <div class="absolute bottom-0 left-0 -ml-20 -mb-20 w-1/3 h-1/3 bg-secondary-100/50 rounded-full blur-3xl opacity-50"></div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center">
          <h2 class="text-5xl md:text-7xl text-gray-900 mb-6 leading-tight">
            Célébrez votre amour avec <br/> 
            <span class="text-primary-600 italic">élégance et simplicité.</span>
          </h2>
          <p class="text-xl text-gray-500 font-sans max-w-2xl mx-auto mb-10 leading-relaxed">
            Créez une invitation digitale sublime, gérez vos invités et organisez votre plan de table en quelques clics.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <router-link to="/register" class="px-8 py-4 bg-primary-600 text-white rounded-full text-lg font-medium hover:bg-primary-700 transition-all shadow-lg shadow-primary-600/30 font-sans">Créer ma carte maintenant</router-link>
            <a href="#concept" class="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-full text-lg font-medium hover:bg-gray-50 transition-all font-sans">Voir un exemple</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section (Concept) -->
    <section id="concept" class="py-24 bg-primary-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl text-gray-900 mb-4">Une expérience complète</h2>
          <p class="text-gray-500 font-sans max-w-xl mx-auto">De l'envoi de l'invitation à l'organisation du jour J, nous vous accompagnons à chaque étape.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div class="bg-white p-10 rounded-3xl shadow-sm border border-primary-100 text-center hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-gray-900">Cartes Personnalisées</h3>
            <p class="text-gray-500 font-sans text-sm leading-relaxed">Choisissez parmi nos templates raffinés et personnalisez les textes, photos et musiques pour une carte qui vous ressemble.</p>
          </div>
          
          <div class="bg-white p-10 rounded-3xl shadow-sm border border-primary-100 text-center hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-16 h-16 bg-secondary-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-gray-900">Gestion RSVP</h3>
            <p class="text-gray-500 font-sans text-sm leading-relaxed">Collectez les réponses de vos invités en temps réel. Suivez les présences, les accompagnants et les restrictions alimentaires.</p>
          </div>
          
          <div class="bg-white p-10 rounded-3xl shadow-sm border border-primary-100 text-center hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
            </div>
            <h3 class="text-2xl mb-4 text-gray-900">Plan de Table</h3>
            <p class="text-gray-500 font-sans text-sm leading-relaxed">Organisez vos invités par table avec une interface simple. Exportez et imprimez votre plan de table en un clic.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="tarifs" class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl text-gray-900 mb-4">Des tarifs transparents</h2>
          <p class="text-gray-500 font-sans max-w-xl mx-auto">Choisissez le forfait qui convient à vos besoins.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div v-for="plan in pricingPlans" :key="plan.name" 
            class="relative bg-white rounded-3xl p-10 border transition-all duration-300 flex flex-col h-full hover:shadow-xl"
            :class="plan.popular ? 'border-primary-400 shadow-lg shadow-primary-900/5' : 'border-gray-100'"
          >
            <div v-if="plan.popular" class="absolute top-0 right-10 -translate-y-1/2 bg-primary-600 text-white px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider font-sans">Le plus populaire</div>
            
            <h3 class="text-2xl text-gray-900 mb-2">{{ plan.name }}</h3>
            <div class="flex items-baseline mb-4">
              <span class="text-4xl font-serif text-primary-800">{{ plan.price }}</span>
              <span class="text-gray-400 ml-2 font-sans">/ événement</span>
            </div>
            <p class="text-gray-500 font-sans text-sm mb-8">{{ plan.description }}</p>
            
            <ul class="space-y-4 mb-10 flex-grow">
              <li v-for="feature in plan.features" :key="feature" class="flex items-center text-sm text-gray-600 font-sans">
                <svg class="w-5 h-5 text-primary-500 mr-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ feature }}
              </li>
            </ul>
            
            <router-link to="/register" 
              class="w-full py-4 rounded-xl text-center font-medium transition-all font-sans"
              :class="plan.popular ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-md shadow-primary-600/20' : 'bg-primary-50 text-primary-800 hover:bg-primary-100 border border-primary-200'"
            >
              {{ plan.cta }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-50 py-12 border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-2xl text-primary-800 mb-4">Saas Wedding</h2>
        <p class="text-gray-400 font-sans text-sm mb-8">© 2026 Saas Wedding - Invitations Digitales & Gestion de Mariage</p>
        <div class="flex justify-center space-x-6 text-gray-400 font-sans text-xs">
          <a href="#" class="hover:text-primary-600">Mentions Légales</a>
          <a href="#" class="hover:text-primary-600">Confidentialité</a>
          <a href="#" class="hover:text-primary-600">Contact</a>
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
