<script setup>
import { ref, computed } from 'vue';
import api from '../../service/api';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true }
});

// --- ÉTAT DU FORMULAIRE ---
const rsvp = ref({
  name: '',
  email: '',
  attending: 'yes',
  guests_count: 0,
  diet: 'Aucun',
  message: ''
});

const isSubmitted = ref(false);
const isLoading = ref(false);
const error = ref('');

// --- LOGIQUE D'AFFICHAGE ET CONTRASTE ---
const theme = computed(() => props.config.theme);
const content = computed(() => props.config.content);

// Calcul de luminance pour le bouton (WCAG AA)
function isDark(hex) {
  if (!hex) return false;
  const r = parseInt(hex.slice(1,3), 16) / 255;
  const g = parseInt(hex.slice(3,5), 16) / 255;
  const b = parseInt(hex.slice(5,7), 16) / 255;
  const L = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return L < 0.5;
}

const labelColor = computed(() => (theme.value.text || '#1A1A1A') + 'B3'); // 70% opacité hex
const buttonTextColor = computed(() => isDark(theme.value.accent) ? '#FFFFFF' : '#1A1A1A');

// --- ACTIONS ---
const validate = () => {
  if (rsvp.value.name.trim().length < 2) return "Veuillez entrer votre nom complet.";
  if (rsvp.value.email && !/^\S+@\S+\.\S+$/.test(rsvp.value.email)) return "Format d'email invalide.";
  return null;
};

const submitRSVP = async () => {
  error.value = '';
  const validationError = validate();
  if (validationError) { error.value = validationError; return; }

  try {
    isLoading.value = true;
    const nameParts = rsvp.value.name.trim().split(' ');
    const first = nameParts[0] || '';
    const last = nameParts.slice(1).join(' ') || '.';
    
    await api.post('/guests/public/rsvp', {
      event_id: props.event.id,
      first_name: first,
      last_name: last,
      email: rsvp.value.email,
      presence: rsvp.value.attending === 'yes',
      adults: parseInt(rsvp.value.guests_count) + 1,
      message: rsvp.value.message
    });
    
    isSubmitted.value = true;
  } catch (err) {
    if (err.response?.status === 403) error.value = "Cette invitation n'est pas encore publiée.";
    else error.value = "Erreur réseau. Veuillez réessayer plus tard.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <section class="rsvp-section py-20 px-6 max-w-xl mx-auto transition-all duration-700">
    <!-- ÉTAT : CONFIRMATION -->
    <div v-if="isSubmitted" class="text-center space-y-6 animate-fadeIn">
      <svg viewBox="0 0 60 60" class="w-20 h-20 mx-auto">
        <circle cx="30" cy="30" r="28" :stroke="theme.accent" stroke-width="1.5" fill="none" class="draw-circle" />
        <path d="M18 30 L26 38 L42 22" :stroke="theme.accent" stroke-width="2" fill="none" stroke-linecap="round" class="draw-check" />
      </svg>
      <h3 class="text-3xl font-light italic" :style="{ color: theme.text }">Merci {{ rsvp.name.split(' ')[0] }}</h3>
      <p :style="{ color: labelColor }">
        {{ rsvp.attending === 'yes' ? 'Votre présence est confirmée !' : 'Nous avons bien reçu votre réponse.' }}
      </p>
    </div>

    <!-- ÉTAT : FORMULAIRE -->
    <form v-else @submit.prevent="submitRSVP" class="space-y-10">
      <h2 class="text-center text-4xl font-serif italic mb-12" :style="{ color: theme.text }">
        {{ content.rsvp_title || 'Serez-vous des nôtres ?' }}
      </h2>

      <!-- Nom -->
      <div class="group relative">
        <label class="block text-[11px] uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor }">Nom Complet</label>
        <input v-model="rsvp.name" type="text" required class="w-full bg-transparent border-b py-2 focus:outline-none transition-colors"
               :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
      </div>

      <!-- Email -->
      <div class="group relative">
        <label class="block text-[11px] uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor }">Email (Optionnel)</label>
        <input v-model="rsvp.email" type="email" class="w-full bg-transparent border-b py-2 focus:outline-none"
               :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
      </div>

      <!-- Toggle Présence -->
      <div class="space-y-4">
        <label class="block text-[11px] uppercase tracking-widest font-medium" :style="{ color: labelColor }">Votre présence</label>
        <div class="flex rounded-full border p-1" :style="{ borderColor: (theme.accent || '#000') + '33' }">
          <button type="button" @click="rsvp.attending = 'yes'" class="flex-1 py-3 rounded-full text-xs font-bold transition-all duration-300"
                  :style="rsvp.attending === 'yes' ? { backgroundColor: theme.accent, color: buttonTextColor } : { color: theme.text }">
            ✓ PRÉSENT(E)
          </button>
          <button type="button" @click="rsvp.attending = 'no'" class="flex-1 py-3 rounded-full text-xs font-bold transition-all duration-300"
                  :style="rsvp.attending === 'no' ? { backgroundColor: theme.text, color: theme.background } : { color: theme.text }">
            ✗ ABSENT(E)
          </button>
        </div>
      </div>

      <!-- Champs Conditionnels -->
      <div v-if="rsvp.attending === 'yes'" class="space-y-10 animate-slideDown">
        <div class="flex flex-col md:flex-row gap-6">
          <div class="flex-1">
            <label class="block text-[11px] uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor }">Accompagnants</label>
            <select v-model="rsvp.guests_count" class="w-full bg-transparent border-b py-2 focus:outline-none" :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
              <option v-for="n in 4" :key="n-1" :value="n-1" class="text-black">{{ n-1 }} personne{{ n > 2 ? 's' : '' }}</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="block text-[11px] uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor }">Régime</label>
            <select v-model="rsvp.diet" class="w-full bg-transparent border-b py-2 focus:outline-none" :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
              <option class="text-black">Aucun</option>
              <option class="text-black">Végétarien</option>
              <option class="text-black">Vegan</option>
              <option class="text-black">Sans Gluten</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Message -->
      <div class="group relative">
        <label class="block text-[11px] uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor }">Un mot pour nous ?</label>
        <textarea v-model="rsvp.message" rows="2" class="w-full bg-transparent border-b py-2 focus:outline-none resize-none"
                  :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }"></textarea>
      </div>

      <!-- Erreur & Submit -->
      <p v-if="error" class="text-red-500 text-xs text-center font-bold tracking-tight">{{ error }}</p>
      
      <button type="submit" :disabled="isLoading" class="w-full py-5 rounded-sm font-bold tracking-[0.2em] transition-all hover:opacity-90 active:scale-[0.98]"
              :style="{ backgroundColor: theme.accent, color: buttonTextColor }">
        {{ isLoading ? 'ENVOI...' : 'CONFIRMER MA RÉPONSE' }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.draw-circle { stroke-dasharray: 176; stroke-dashoffset: 0; }
.draw-check { stroke-dasharray: 30; stroke-dashoffset: 30; animation: draw 0.6s 0.4s ease forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fadeIn { animation: fadeIn 0.8s ease-out; }
.animate-slideDown { animation: fadeIn 0.4s ease-out; }
</style>
