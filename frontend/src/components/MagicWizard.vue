<script setup>
import { ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useWizardStore } from '../stores/wizard.js';

const router = useRouter();
const wizard = useWizardStore();
wizard.step = 1;

// ─── Transition directionnelle ────────────────────────────────────────────────
const direction = ref(1); // 1 = avant, -1 = arrière
const transitionName = computed(() => direction.value === 1 ? 'slide-fwd' : 'slide-back');

const goNext = () => { direction.value =  1; wizard.next(); };
const goPrev = () => {
  if (wizard.step === 1) { router.back(); return; }
  direction.value = -1;
  wizard.prev();
};

const finish = (style = null) => {
  if (style !== null) wizard.style = style;
  wizard.save();
  router.push('/templates');
};

// ─── Date minimum = aujourd'hui
const today     = new Date().toISOString().split('T')[0];
const dateError = ref('');

const onDateChange = () => {
  if (wizard.date && wizard.date < today) {
    dateError.value = 'La date doit être dans le futur. ✨';
    wizard.date = '';
    setTimeout(() => { dateError.value = ''; }, 3000);
  }
};

// ─── Autocomplétion adresse (api-adresse.data.gouv.fr) ────────────────────────
const locationSuggestions = ref([]);
const showSuggestions     = ref(false);
let   searchTimer         = null;

const onLocationInput = () => {
  clearTimeout(searchTimer);
  if (!wizard.location || wizard.location.length < 2) {
    locationSuggestions.value = [];
    showSuggestions.value     = false;
    return;
  }
  searchTimer = setTimeout(async () => {
    try {
      const q   = encodeURIComponent(wizard.location);
      const res = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${q}&limit=5`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      locationSuggestions.value = data.features?.map(f => f.properties.label) ?? [];
      showSuggestions.value     = locationSuggestions.value.length > 0;
    } catch {
      locationSuggestions.value = [];
      showSuggestions.value     = false;
    }
  }, 300);
};

const selectSuggestion = (label) => {
  wizard.location           = label;
  locationSuggestions.value = [];
  showSuggestions.value     = false;
};

const closeSuggestions = () => {
  setTimeout(() => { showSuggestions.value = false; }, 150);
};

onUnmounted(() => clearTimeout(searchTimer));

// ─── Styles disponibles ───────────────────────────────────────────────────────
const styles = [
  { id: 'all',     name: 'Tous les templates', description: 'Voir toute la collection',          icon: '✨' },
  { id: 'minimal', name: 'Luxe Minimaliste',   description: 'Épuré, moderne et intemporel',      icon: '🕊️' },
  { id: 'classic', name: 'Classique Royal',    description: 'Traditionnel, doré et majestueux',  icon: '👑' },
  { id: 'art',     name: 'Art & Culture',      description: 'Graphique, audacieux et original',  icon: '🎨' },
  { id: 'boho',    name: 'Bohème Chic',        description: 'Naturel, floral et poétique',       icon: '🌿' },
];

// ─── Validation par étape ─────────────────────────────────────────────────────
const progress = computed(() => (wizard.step / 4) * 100);
const canStep1 = computed(() => !!wizard.groomName.trim() && !!wizard.brideName.trim());
const canStep2 = computed(() => !!wizard.date);
const canStep3 = computed(() => !!wizard.location.trim());
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] flex flex-col items-center justify-center px-4 py-16
              relative overflow-hidden font-serif">

    <!-- Barre de progression -->
    <div class="absolute top-0 left-0 w-full h-1 bg-gray-100">
      <div class="h-full bg-[#C5A059] transition-all duration-700 ease-out"
           :style="{ width: progress + '%' }"/>
    </div>

    <!-- Bouton Retour — toujours visible, haut-gauche -->
    <button
      @click="goPrev"
      class="absolute top-5 left-5 z-20 flex items-center gap-2
             text-gray-400 hover:text-[#1A1A1A] transition-colors group"
      :aria-label="wizard.step === 1 ? 'Quitter' : 'Étape précédente'"
    >
      <svg class="w-5 h-5 transition-transform group-hover:-translate-x-1 duration-200"
           fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
      </svg>
      <span class="text-xs uppercase tracking-widest hidden sm:inline">
        {{ wizard.step === 1 ? 'Quitter' : 'Retour' }}
      </span>
    </button>

    <!-- Indicateur étape -->
    <p class="absolute top-6 right-6 text-[10px] uppercase tracking-[0.3em] text-gray-300 font-sans">
      {{ wizard.step }} / 4
    </p>

    <!-- Contenu principal -->
    <div class="w-full max-w-4xl">
      <Transition :name="transitionName" mode="out-in">
        <div :key="wizard.step" class="w-full">

          <!-- ─────────────────────────────────────────────────────────────────
               ÉTAPE 1 — Prénoms + preview live
          ───────────────────────────────────────────────────────────────── -->
          <div v-if="wizard.step === 1"
               class="flex flex-col items-center">

            <!-- Formulaire -->
            <div class="w-full max-w-xl space-y-10 text-center">
              <div class="space-y-3">
                <span class="text-[#C5A059] tracking-[0.3em] text-xs uppercase">L'Identité</span>
                <h2 class="text-4xl md:text-5xl text-[#1A1A1A] leading-tight">
                  À qui est dédiée cette magnifique journée ?
                </h2>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="space-y-2">
                  <label class="block text-[10px] uppercase tracking-widest text-gray-400">
                    Prénom 1 (La Mariée)
                  </label>
                  <input
                    v-model="wizard.groomName"
                    type="text"
                    placeholder="Ex : Alexandre"
                    autocomplete="off"
                    class="w-full bg-transparent border-b-2 border-gray-200 py-3 text-2xl
                           focus:border-[#C5A059] outline-none transition-colors text-center"
                  />
                </div>
                <div class="space-y-2">
                  <label class="block text-[10px] uppercase tracking-widest text-gray-400">
                    Prénom 2 (La Marié)
                  </label>
                  <input
                    v-model="wizard.brideName"
                    type="text"
                    placeholder="Ex : Éléonore"
                    autocomplete="off"
                    class="w-full bg-transparent border-b-2 border-gray-200 py-3 text-2xl
                           focus:border-[#C5A059] outline-none transition-colors text-center"
                  />
                </div>
              </div>

              <button
                @click="goNext"
                :disabled="!canStep1"
                class="px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-sm
                       hover:bg-black transition-all disabled:opacity-30
                       tracking-widest uppercase"
              >
                Continuer
              </button>
            </div>

          </div>

          <!-- ─────────────────────────────────────────────────────────────────
               ÉTAPE 2 — Date
          ───────────────────────────────────────────────────────────────── -->
          <div v-else-if="wizard.step === 2"
               class="max-w-2xl mx-auto text-center space-y-10">
            <div class="space-y-3">
              <span class="text-[#C5A059] tracking-[0.3em] text-xs uppercase">Le Temps</span>
              <h2 class="text-4xl md:text-5xl text-[#1A1A1A] leading-tight">
                Quel est le moment tant attendu où vous vous direz enfin OUI ?
              </h2>
            </div>

            <div class="space-y-2">
              <input
                v-model="wizard.date"
                type="date"
                :min="today"
                @change="onDateChange"
                class="w-full max-w-sm mx-auto block bg-transparent border-b-2 border-gray-200
                       py-4 text-3xl focus:border-[#C5A059] outline-none transition-colors
                       text-center cursor-pointer"
              />
              <Transition name="fade">
                <p v-if="dateError"
                   class="text-red-400 text-sm font-sans tracking-wide mt-2">
                  {{ dateError }}
                </p>
              </Transition>
            </div>

            <button
              @click="goNext"
              :disabled="!canStep2"
              class="px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-sm
                     hover:bg-black transition-all disabled:opacity-30
                     tracking-widest uppercase"
            >
              Suivant
            </button>
          </div>

          <!-- ─────────────────────────────────────────────────────────────────
               ÉTAPE 3 — Lieu + autocomplétion
          ───────────────────────────────────────────────────────────────── -->
          <div v-else-if="wizard.step === 3"
               class="max-w-2xl mx-auto text-center space-y-10">
            <div class="space-y-3">
              <span class="text-[#C5A059] tracking-[0.3em] text-xs uppercase">Le Lieu</span>
              <h2 class="text-4xl md:text-5xl text-[#1A1A1A] leading-tight">
                Dans quel lieu magique vos souvenirs prendront-ils vie ?
              </h2>
            </div>

            <div class="max-w-xl mx-auto relative text-left">
              <input
                v-model="wizard.location"
                type="text"
                placeholder="Ex : Château de Versailles, France"
                autocomplete="off"
                @input="onLocationInput"
                @blur="closeSuggestions"
                @keydown.escape="showSuggestions = false"
                class="w-full bg-transparent border-b-2 border-gray-200 py-4 text-2xl
                       focus:border-[#C5A059] outline-none transition-colors text-center"
              />

              <!-- Suggestions -->
              <Transition name="fade">
                <ul v-if="showSuggestions && locationSuggestions.length"
                    class="absolute left-0 right-0 top-full mt-2 bg-white rounded-xl shadow-xl
                           border border-gray-100 overflow-hidden z-50 font-sans"
                    @mousedown.prevent>
                  <li v-for="s in locationSuggestions"
                      :key="s"
                      @click="selectSuggestion(s)"
                      class="px-5 py-3 text-sm text-[#1A1A1A] hover:bg-[#F9F7F2] cursor-pointer
                             border-b border-gray-50 last:border-0 flex items-center gap-3
                             transition-colors">
                    <svg class="w-3.5 h-3.5 text-[#C5A059] shrink-0"
                         fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    {{ s }}
                  </li>
                </ul>
              </Transition>

              <p class="mt-3 text-center text-[10px] uppercase tracking-widest text-gray-300 font-sans">
                Saisissez librement pour un lieu hors de France
              </p>
            </div>

            <button
              @click="goNext"
              :disabled="!canStep3"
              class="px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-sm
                     hover:bg-black transition-all disabled:opacity-30
                     tracking-widest uppercase"
            >
              Suivant
            </button>
          </div>

          <!-- ─────────────────────────────────────────────────────────────────
               ÉTAPE 4 — Atmosphère
          ───────────────────────────────────────────────────────────────── -->
          <div v-else-if="wizard.step === 4"
               class="max-w-3xl mx-auto text-center space-y-10">
            <div class="space-y-3">
              <span class="text-[#C5A059] tracking-[0.3em] text-xs uppercase">L'Ambiance</span>
              <h2 class="text-4xl md:text-5xl text-[#1A1A1A] leading-tight">
                Quel ton souhaitez-vous donner à cette journée unique ?
              </h2>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              <div
                v-for="s in styles"
                :key="s.id"
                @click="finish(s.id)"
                class="group cursor-pointer p-6 bg-white border rounded-2xl
                       hover:border-[#C5A059] transition-all duration-300
                       hover:shadow-2xl hover:shadow-[#C5A059]/10 hover:-translate-y-1"
                :class="s.id === 'all'
                  ? 'border-[#C5A059]/30 bg-[#C5A059]/5'
                  : 'border-gray-100'"
              >
                <div class="text-3xl mb-3 transition-transform duration-500 group-hover:scale-125">
                  {{ s.icon }}
                </div>
                <h3 class="text-sm mb-1 leading-tight">{{ s.name }}</h3>
                <p class="text-[11px] text-gray-400 font-sans leading-snug">{{ s.description }}</p>
              </div>
            </div>

            <p class="text-[11px] text-gray-300 font-sans italic tracking-wide">
              Vous pourrez revenir en arrière à tout moment pour modifier vos choix.
            </p>
          </div>

        </div>
      </Transition>
    </div>

    <!-- Citation de fond -->
    <div class="absolute bottom-8 left-0 right-0 text-center
                text-gray-300 italic text-xs tracking-widest opacity-50 font-sans px-4">
      "L'esthétique de ce jour sera le miroir de votre complicité."
    </div>
  </div>
</template>

<style scoped>
/* Slide vers l'avant (nouvelle étape entre par la droite) */
.slide-fwd-enter-active,
.slide-fwd-leave-active {
  transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fwd-enter-from  { opacity: 0; transform: translateX(32px); }
.slide-fwd-leave-to    { opacity: 0; transform: translateX(-32px); }

/* Slide vers l'arrière (nouvelle étape entre par la gauche) */
.slide-back-enter-active,
.slide-back-leave-active {
  transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-back-enter-from  { opacity: 0; transform: translateX(-32px); }
.slide-back-leave-to    { opacity: 0; transform: translateX(32px); }

/* Fade pour les messages d'erreur */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from,   .fade-leave-to     { opacity: 0; }

input::placeholder { color: #E5E5E5; }
</style>
