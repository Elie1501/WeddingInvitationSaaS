<template>
  <!-- Backdrop -->
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[200] flex items-center justify-center p-4"
        @click.self="$emit('update:modelValue', false)"
      >
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" />

        <!-- Panel -->
        <div class="relative z-10 w-full max-w-lg bg-white rounded-3xl shadow-2xl overflow-hidden max-h-[90vh] overflow-y-auto">

          <!-- Header -->
          <div class="bg-gradient-to-r from-primary-700 to-primary-500 px-6 sm:px-8 py-6 text-white">
            <button
              class="absolute top-4 right-4 text-white/70 hover:text-white transition-colors"
              @click="$emit('update:modelValue', false)"
            >
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <p class="text-primary-200 text-sm font-medium tracking-widest uppercase mb-1">Passez au niveau supérieur</p>
            <h2 class="text-2xl font-serif font-bold">Forfait Premium</h2>
            <p class="mt-1 text-primary-100 text-sm">Débloquez tout pour votre grand jour</p>
          </div>

          <!-- Comparison -->
          <div class="px-6 sm:px-8 py-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-6">

              <!-- Classic column -->
              <div class="rounded-2xl border border-gray-200 p-4">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Classic</p>
                <ul class="space-y-2 text-sm text-gray-600">
                  <li v-for="feat in classicFeatures" :key="feat" class="flex items-start gap-2">
                    <svg class="w-4 h-4 text-green-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                    {{ feat }}
                  </li>
                  <li v-for="feat in blockedFeatures" :key="feat" class="flex items-start gap-2 opacity-40">
                    <svg class="w-4 h-4 text-gray-400 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    {{ feat }}
                  </li>
                </ul>
                <p class="mt-4 text-lg font-bold text-gray-700">29 €</p>
              </div>

              <!-- Premium column -->
              <div class="rounded-2xl border-2 border-primary-400 bg-primary-50 p-4 relative">
                <span class="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-primary-500 text-white text-[10px] font-bold px-3 py-0.5 rounded-full uppercase tracking-wide">Recommandé</span>
                <p class="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">Premium</p>
                <ul class="space-y-2 text-sm text-gray-700">
                  <li v-for="feat in [...classicFeatures, ...blockedFeatures]" :key="feat" class="flex items-start gap-2">
                    <svg class="w-4 h-4 text-primary-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                    </svg>
                    {{ feat }}
                  </li>
                </ul>
                <p class="mt-4 text-lg font-bold text-primary-700">79 €</p>
              </div>
            </div>

            <!-- CTA -->
            <div class="text-center">
              <p class="text-sm text-gray-500 mb-3">
                Vous avez déjà payé le forfait Classic.
                <br />Payez simplement la <strong class="text-primary-700">différence : 50 €</strong>
              </p>
              <button
                :disabled="loading"
                class="w-full py-3.5 rounded-2xl bg-primary-500 hover:bg-primary-600 text-white font-semibold
                       text-base transition-all duration-200 shadow-lg hover:shadow-primary-300/50
                       disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                @click="startUpgrade"
              >
                <svg v-if="loading" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                </svg>
                {{ loading ? 'Redirection vers Stripe…' : 'Passer Premium pour 50 €' }}
              </button>

              <!-- Bloc erreur avec retry -->
              <div v-if="errorMsg" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-left">
                <p class="text-xs font-black uppercase tracking-widest text-red-700 mb-1">Erreur de paiement</p>
                <p class="text-sm text-red-600">{{ errorMsg }}</p>
                <button @click="startUpgrade"
                        class="mt-2 text-xs font-bold text-red-700 underline hover:text-red-900 transition-colors">
                  Réessayer
                </button>
              </div>

              <button
                class="mt-3 text-xs text-gray-400 hover:text-gray-600 underline transition-colors"
                @click="$emit('update:modelValue', false)"
              >
                Continuer avec Classic
              </button>
            </div>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import api from '../service/api';

const props = defineProps({
  modelValue: { type: Boolean, required: true },
  cardId: { type: [Number, String], default: null },
});
const emit = defineEmits(['update:modelValue']);

const loading = ref(false);
const errorMsg = ref('');
const isDev = import.meta.env.DEV;

const classicFeatures = [
  "1 site d'invitation",
  'Formulaire RSVP',
  'Plan de table interactif',
  "Musique d'ambiance",
  'Personnalisation complète',
];

const blockedFeatures = [
  "Jusqu'à 5 sites d'invitation",
  'Tous les templates Premium',
  'Blocs de personnalisation Premium',
  'Typographie personnalisée',
  'Export CSV des invités',
];

const startUpgrade = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const url = props.cardId
      ? `/payments/create-upgrade-session?card_id=${props.cardId}`
      : '/payments/create-upgrade-session';
    const res = await api.post(url);
    if (res.data.checkout_url) {
      window.location.href = res.data.checkout_url;
    }
  } catch (err) {
    const detail = err.response?.data?.detail;
    errorMsg.value = isDev && detail
      ? `[DEV] ${detail}`
      : "Impossible d'initialiser le paiement. Veuillez réessayer.";
    console.error('Upgrade error:', err);
    loading.value = false;
  }
};
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
