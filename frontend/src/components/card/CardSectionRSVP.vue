<script setup>
import { ref, computed, watch } from 'vue';
import api from '../../service/api';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true }
});

// --- ÉTAT DU FORMULAIRE ---
const persons = ref([{ first_name: '', last_name: '', dietary_restrictions: '' }]);
const rsvp = ref({ attending: 'yes', message: '' });

const isSubmitted = ref(false);
const isLoading = ref(false);
const error = ref('');

// Vider les personnes supplémentaires quand on bascule sur "absent"
watch(() => rsvp.value.attending, (val) => {
  if (val === 'no') persons.value = [persons.value[0]];
});

// --- LOGIQUE D'AFFICHAGE ET CONTRASTE ---
const theme = computed(() => props.config.theme);
const content = computed(() => props.config.content);

function isDark(hex) {
  if (!hex) return false;
  const r = parseInt(hex.slice(1,3), 16) / 255;
  const g = parseInt(hex.slice(3,5), 16) / 255;
  const b = parseInt(hex.slice(5,7), 16) / 255;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.5;
}

const labelColor = computed(() => (theme.value.text || '#1A1A1A') + 'B3');
const buttonTextColor = computed(() => isDark(theme.value.accent) ? '#FFFFFF' : '#1A1A1A');

// --- Gestion liste personnes ---
const addPerson = () => {
  if (persons.value.length < 30) {
    persons.value.push({ first_name: '', last_name: '', dietary_restrictions: '' });
  }
};
const removePerson = (i) => { if (persons.value.length > 1) persons.value.splice(i, 1); };

// --- VALIDATION ---
const validate = () => {
  for (let i = 0; i < persons.value.length; i++) {
    const p = persons.value[i];
    if (!p.first_name.trim()) return i === 0 ? 'Veuillez entrer votre prénom.' : `Prénom requis pour la personne ${i + 1}.`;
    if (!p.last_name.trim())  return i === 0 ? 'Veuillez entrer votre nom.' : `Nom requis pour la personne ${i + 1}.`;
  }
  return null;
};

// --- SOUMISSION ---
const submitRSVP = async () => {
  error.value = '';
  const validationError = validate();
  if (validationError) { error.value = validationError; return; }

  try {
    isLoading.value = true;
    const attending = rsvp.value.attending === 'yes';
    const main = persons.value[0];

    await api.post('/guests/public/rsvp', {
      event_id: props.event.id,
      first_name: main.first_name.trim(),
      last_name: main.last_name.trim(),
      presence: attending,
      dietary_restrictions: main.dietary_restrictions || null,
      sub_guests: attending
        ? persons.value.slice(1).map(p => ({
            first_name: p.first_name.trim(),
            last_name: p.last_name.trim(),
            dietary_restrictions: p.dietary_restrictions || null
          }))
        : [],
      message: rsvp.value.message || null,
    });

    isSubmitted.value = true;
  } catch (err) {
    if (err.response?.status === 403) error.value = "Cette invitation n'est pas encore publiée.";
    else if (err.response?.status === 422) error.value = "Données invalides. Vérifiez les champs et réessayez.";
    else error.value = "Erreur réseau. Veuillez réessayer plus tard.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <section class="rsvp-section py-20 px-6 max-w-xl mx-auto transition-all duration-700" :style="{ fontFamily: theme.fontFamily }">

    <!-- ÉTAT : CONFIRMATION -->
    <div v-if="isSubmitted" class="text-center space-y-6 animate-fadeIn">
      <svg viewBox="0 0 60 60" class="w-20 h-20 mx-auto">
        <circle cx="30" cy="30" r="28" :stroke="theme.accent" stroke-width="1.5" fill="none" class="draw-circle" />
        <path d="M18 30 L26 38 L42 22" :stroke="theme.accent" stroke-width="2" fill="none" stroke-linecap="round" class="draw-check" />
      </svg>
      <h3 class="font-light italic" :style="{ color: theme.text, fontSize: 'var(--size-headings, 1.875rem)', fontFamily: theme.fontFamily }">
        Merci {{ persons[0].first_name }}
      </h3>
      <p :style="{ color: labelColor }">
        {{ rsvp.attending === 'yes' ? 'Votre présence est confirmée !' : 'Nous avons bien reçu votre réponse.' }}
      </p>
    </div>

    <!-- ÉTAT : FORMULAIRE -->
    <form v-else @submit.prevent="submitRSVP" class="space-y-10">
      <h2 class="text-center italic mb-4" :style="{ color: 'var(--color-section-title)', fontSize: 'var(--size-headings, 2.25rem)', fontFamily: theme.fontFamily }">
        {{ content.rsvp_title || 'Serez-vous des nôtres ?' }}
      </h2>
      <p v-if="content.rsvp_deadline_text" class="text-center mb-10 italic" :style="{ color: labelColor, fontSize: 'var(--size-body, 0.875rem)', fontFamily: theme.fontFamily }">
        {{ content.rsvp_deadline_text }}
      </p>

      <!-- Toggle Présence -->
      <div class="space-y-4">
        <label class="block uppercase tracking-widest font-medium" :style="{ color: labelColor, fontSize: 'var(--size-label, 0.7rem)' }">Votre présence</label>
        <div class="flex rounded-full border p-1" :style="{ borderColor: (theme.accent || '#000') + '33' }">
          <button type="button" @click="rsvp.attending = 'yes'" class="flex-1 py-3 rounded-full font-bold transition-all duration-300" style="font-size: var(--size-label, 0.7rem)"
                  :style="rsvp.attending === 'yes' ? { backgroundColor: theme.accent, color: buttonTextColor } : { color: theme.text }">
            ✓ PRÉSENT(E)
          </button>
          <button type="button" @click="rsvp.attending = 'no'" class="flex-1 py-3 rounded-full font-bold transition-all duration-300" style="font-size: var(--size-label, 0.7rem)"
                  :style="rsvp.attending === 'no' ? { backgroundColor: theme.text, color: theme.background } : { color: theme.text }">
            ✗ ABSENT(E)
          </button>
        </div>
      </div>

      <!-- Liste des personnes -->
      <div class="space-y-6 animate-slideDown">
        <label class="block uppercase tracking-widest font-medium" :style="{ color: labelColor, fontSize: 'var(--size-label, 0.7rem)' }">
          {{ rsvp.attending === 'yes' ? 'Personnes présentes' : 'Votre identité' }}
        </label>

        <div v-for="(person, idx) in persons" :key="idx"
             class="space-y-3 pb-4"
             :class="idx > 0 ? 'border-t pt-4' : ''"
             :style="idx > 0 ? { borderColor: (theme.accent || '#000') + '22' } : {}">

          <!-- En-tête personne -->
          <div class="flex items-center justify-between">
            <span class="uppercase tracking-widest font-bold" :style="{ color: labelColor, fontSize: 'var(--size-label, 0.65rem)' }">
              {{ idx === 0 ? 'Vous' : 'Personne ' + (idx + 1) }}
            </span>
            <button v-if="idx > 0" type="button" @click="removePerson(idx)"
                    class="text-[10px] uppercase tracking-wider font-bold transition-opacity hover:opacity-70"
                    :style="{ color: theme.text + '66' }">
              Retirer
            </button>
          </div>

          <!-- Prénom / Nom (champs séparés pour faciliter la saisie sur mobile) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input v-model="person.first_name" type="text" placeholder="Prénom" required
                   class="w-full bg-transparent border-b py-2.5 focus:outline-none"
                   style="font-size: var(--size-body, 0.875rem)"
                   :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
            <input v-model="person.last_name" type="text" placeholder="Nom" required
                   class="w-full bg-transparent border-b py-2.5 focus:outline-none"
                   style="font-size: var(--size-body, 0.875rem)"
                   :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
          </div>

          <!-- Régime (seulement si présent) -->
          <div v-if="rsvp.attending === 'yes'">
            <select v-model="person.dietary_restrictions"
                    class="w-full bg-transparent border-b py-2 focus:outline-none"
                    style="font-size: var(--size-body, 0.875rem)"
                    :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }">
              <option value="" class="text-black">Aucun régime particulier</option>
              <option class="text-black">Végétarien</option>
              <option class="text-black">Vegan</option>
              <option class="text-black">Sans Gluten</option>
            </select>
          </div>
        </div>

        <!-- Bouton + Ajouter une personne -->
        <button v-if="rsvp.attending === 'yes' && persons.length < 30"
                type="button"
                @click="addPerson"
                class="w-full py-3 rounded-full border font-bold tracking-widest uppercase transition-all hover:opacity-80"
                style="font-size: var(--size-label, 0.7rem)"
                :style="{ borderColor: (theme.accent || '#000') + '44', color: theme.accent || theme.text }">
          + Ajouter une personne
        </button>
      </div>

      <!-- Message -->
      <div class="group relative">
        <label class="block uppercase tracking-widest font-medium mb-1" :style="{ color: labelColor, fontSize: 'var(--size-label, 0.7rem)' }">Un mot pour nous ?</label>
        <textarea v-model="rsvp.message" rows="2" class="w-full bg-transparent border-b py-2 focus:outline-none resize-none"
                  style="font-size: var(--size-body, 0.875rem)"
                  :style="{ borderBottomColor: (theme.accent || '#000') + '4D', color: theme.text }"></textarea>
      </div>

      <!-- Erreur & Submit -->
      <p v-if="error" class="text-red-500 text-xs text-center font-bold tracking-tight">{{ error }}</p>

      <button type="submit" :disabled="isLoading" class="w-full py-5 rounded-sm font-bold tracking-[0.2em] transition-all hover:opacity-90 active:scale-[0.98]"
              style="font-size: var(--size-label, 0.75rem)"
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
