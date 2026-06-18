<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import api from '../service/api';

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const { notifyError, notifyWarning } = useToast();

const loadingPlan = ref(null);

const plans = [
  {
    id: 'classic',
    name: 'Classic',
    price: '29 €',
    tagline: "L'essentiel pour votre mariage",
    features: ['1 site web', 'Formulaire RSVP', 'Plan de table', 'Personnalisation complète'],
    highlight: false,
  },
  {
    id: 'premium',
    name: 'Premium',
    price: '79 €',
    tagline: 'Expérience complète et personnalisée',
    features: ['Tout le Classic', 'Templates Premium', 'Compte à rebours & programme', 'Musique de fond', "Jusqu'à 5 sites web", 'Export CSV invités'],
    highlight: true,
  },
];

const choosePlan = async (planId) => {
  loadingPlan.value = planId;
  try {
    const res = await api.post('/payments/create-checkout-session', { plan_name: planId });
    if (res.data.checkout_url) {
      window.location.href = res.data.checkout_url;
      return;
    }
    throw new Error('checkout_url manquant');
  } catch (err) {
    notifyError(err, { fallback: "Impossible d'ouvrir le paiement. Veuillez réessayer." });
    loadingPlan.value = null;
  }
};

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};

onMounted(async () => {
  if (!auth.user) await auth.fetchMe();
  // Un compte déjà payé n'a rien à faire ici → on l'envoie au dashboard.
  if (auth.user && ['classic', 'premium'].includes(auth.user.plan)) {
    router.replace('/dashboard');
    return;
  }
  if (route.query.payment_cancel === 'true') {
    notifyWarning('Paiement annulé. Choisissez un forfait pour activer votre compte.');
    router.replace({ query: {} });
  }
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-primary-50 relative overflow-hidden px-4 py-10">
    <!-- Décoration de fond -->
    <div class="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary-200/30 blur-3xl"></div>
    <div class="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-200/30 blur-3xl"></div>

    <div class="w-full max-w-3xl relative z-10">
      <div class="text-center mb-8">
        <h1 class="text-3xl sm:text-4xl text-primary-800 mb-2">Activez votre compte</h1>
        <p class="text-sm text-gray-500 font-sans tracking-wide uppercase">Choisissez votre forfait pour commencer</p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div
          v-for="plan in plans"
          :key="plan.id"
          :class="[
            'relative rounded-3xl bg-white p-6 sm:p-8 border-2 shadow-xl shadow-primary-900/5 flex flex-col',
            plan.highlight ? 'border-primary-500' : 'border-gray-200',
          ]"
        >
          <span
            v-if="plan.highlight"
            class="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-500 text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wide"
          >Recommandé</span>

          <p class="text-xs font-semibold uppercase tracking-widest"
             :class="plan.highlight ? 'text-primary-600' : 'text-gray-400'">{{ plan.name }}</p>
          <p class="text-xs text-gray-500 mt-1 font-sans">{{ plan.tagline }}</p>
          <p class="mt-3 text-3xl font-bold text-gray-900">{{ plan.price }}</p>

          <ul class="mt-5 space-y-2 text-sm text-gray-600 flex-1">
            <li v-for="f in plan.features" :key="f" class="flex items-start gap-2">
              <svg class="w-4 h-4 text-primary-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              {{ f }}
            </li>
          </ul>

          <button
            :disabled="loadingPlan !== null"
            class="mt-6 w-full py-3 rounded-2xl font-semibold transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            :class="plan.highlight
              ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg shadow-primary-600/20'
              : 'bg-gray-900 hover:bg-black text-white'"
            @click="choosePlan(plan.id)"
          >
            <svg v-if="loadingPlan === plan.id" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
            </svg>
            {{ loadingPlan === plan.id ? 'Redirection vers Stripe…' : `Choisir ${plan.name}` }}
          </button>
        </div>
      </div>

      <div class="mt-8 text-center">
        <button class="text-xs text-gray-400 hover:text-gray-600 underline transition-colors" @click="handleLogout">
          Se déconnecter
        </button>
      </div>
    </div>
  </div>
</template>
