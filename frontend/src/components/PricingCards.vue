<script setup lang="ts">
import { ref } from 'vue';
import api from '../service/api';
import { useToast } from '../composables/useToast';

const { notifyError } = useToast();
const loadingPlan = ref<string | null>(null);

const plans = [
  {
    name: 'Classique',
    id: 'classic',
    price: '29€',
    description: 'Parfait pour un petit mariage élégant.',
    features: [
      "1 site d'invitation",
      'Formulaire RSVP',
      'Plan de table interactif',
      "Musique d'ambiance",
      'Personnalisation complète'
    ],
    buttonText: 'Choisir Classique',
    highlight: false
  },
  {
    name: 'Premium',
    id: 'premium',
    price: '79€',
    description: 'L\'expérience ultime pour un grand événement.',
    features: [
      'Tout le Classic',
      "Jusqu'à 5 sites d'invitation",
      'Tous les templates Premium',
      'Blocs de personnalisation Premium',
      'Typographie personnalisée',
      'Export CSV des invités'
    ],
    buttonText: 'Passer au Premium',
    highlight: true
  }
];

const handleSubscription = async (planId: string) => {
  try {
    loadingPlan.value = planId;
    const response = await api.post('/payments/create-checkout-session', {
      plan_name: planId
    });
    
    if (response.data.checkout_url) {
      // Redirection vers l'URL de paiement (ou simulation)
      window.location.href = response.data.checkout_url;
    }
  } catch (error) {
    console.error('Erreur lors de la création de la session de paiement:', error);
    notifyError(error, { fallback: 'Une erreur est survenue. Veuillez réessayer.' });
  } finally {
    loadingPlan.value = null;
  }
};
</script>

<template>
  <div class="py-12 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Choisissez le plan parfait pour votre grand jour
        </h2>
        <p class="mt-4 text-xl text-gray-600">
          Des fonctionnalités simples et puissantes pour organiser votre mariage sans stress.
        </p>
      </div>

      <div class="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-6 lg:max-w-4xl lg:mx-auto xl:max-w-none xl:mx-0 xl:grid-cols-2">
        <div 
          v-for="plan in plans" 
          :key="plan.id"
          :class="[
            'border rounded-2xl shadow-sm divide-y divide-gray-200 bg-white transition-all duration-300 hover:shadow-xl',
            plan.highlight ? 'border-primary-500 ring-2 ring-primary-500' : 'border-gray-200'
          ]"
        >
          <div class="p-8">
            <h3 class="text-2xl font-semibold text-gray-900">{{ plan.name }}</h3>
            <p class="mt-4 text-gray-500">{{ plan.description }}</p>
            <p class="mt-8">
              <span class="text-4xl font-extrabold text-gray-900">{{ plan.price }}</span>
              <span class="text-base font-medium text-gray-500"> / événement</span>
            </p>
            <button
              @click="handleSubscription(plan.id)"
              :disabled="loadingPlan !== null"
              :class="[
                'mt-8 block w-full py-3 px-6 border border-transparent rounded-xl text-center font-semibold transition-colors',
                plan.highlight 
                  ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-md shadow-primary-200' 
                  : 'bg-primary-50 text-primary-700 hover:bg-primary-100',
                loadingPlan === plan.id ? 'opacity-75 cursor-wait' : ''
              ]"
            >
              <span v-if="loadingPlan === plan.id" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Chargement...
              </span>
              <span v-else>{{ plan.buttonText }}</span>
            </button>
          </div>
          <div class="pt-6 pb-8 px-8">
            <h4 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Ce qui est inclus :</h4>
            <ul role="list" class="mt-6 space-y-4">
              <li v-for="feature in plan.features" :key="feature" class="flex space-x-3">
                <svg class="flex-shrink-0 h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span class="text-sm text-gray-600">{{ feature }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
