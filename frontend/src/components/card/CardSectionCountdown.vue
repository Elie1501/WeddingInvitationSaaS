<script setup>
// CardSectionCountdown.vue — Phase 2
// Section partagée. Reçoit config + event (même convention que CardSectionRSVP).
// La logique temporelle vient de useTemplateData : timeLeft réactif à la date.
import { computed } from 'vue';
import { useTemplateData } from '@/composables/useTemplateData';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true },
});

// Comportement factorisé (timer + recalcul live si la date change)
const { timeLeft } = useTemplateData(() => props.config, () => props.event);

// Lecture directe config/event — comme RSVP
const theme   = computed(() => props.config.theme   || {});
const content = computed(() => props.config.content || {});

// Couleur des libellés : texte atténué (même recette que RSVP)
const labelColor = computed(() => (theme.value.text || '#1A1A1A') + 'B3');

// Couleur des chiffres : var custom de l'éditeur, fallback sur l'accent du thème.
// Le fallback évite l'écueil "chiffres invisibles si la var n'est pas définie".
const numberColor = computed(
  () => `var(--color-countdown, ${theme.value.accent || theme.value.text || '#1A1A1A'})`
);

const units = computed(() => [
  { value: timeLeft.value.days,  label: 'Jours'  },
  { value: timeLeft.value.hours, label: 'Heures' },
  { value: timeLeft.value.mins,  label: 'Min'    },
  { value: timeLeft.value.secs,  label: 'Sec'    },
]);

const pad = (n) => String(n).padStart(2, '0');
</script>

<template>
  <section
    class="countdown-section py-16 px-6 max-w-xl mx-auto text-center transition-all duration-700"
    :style="{ fontFamily: theme.fontFamily }"
  >
    <!-- Titre optionnel de la section -->
    <h2
      v-if="content.countdown_title"
      class="italic mb-8"
      style="font-size: var(--size-headings, clamp(1.5rem, 6vw, 2.25rem)); overflow-wrap: break-word"
      :style="{ color: `var(--color-section-title, ${theme.text || '#1A1A1A'})`, fontFamily: theme.fontFamily }"
    >
      {{ content.countdown_title }}
    </h2>

    <!-- Jour J atteint -->
    <p
      v-if="timeLeft.isPast"
      class="italic uppercase tracking-[0.2em]"
      style="font-size: var(--size-body, clamp(0.9rem, 4vw, 1.1rem))"
      :style="{ color: numberColor }"
    >
      C'est le grand jour
    </p>

    <!-- Décompte -->
    <div v-else class="grid grid-cols-4 gap-3 sm:gap-5">
      <div v-for="unit in units" :key="unit.label" class="flex flex-col items-center">
        <span
          class="font-light tabular-nums leading-none"
          style="font-size: var(--size-countdown, clamp(1.75rem, 9vw, 3rem))"
          :style="{ color: numberColor }"
        >
          {{ pad(unit.value) }}
        </span>
        <span
          class="mt-2 uppercase tracking-[0.18em]"
          style="font-size: var(--size-label, 0.65rem)"
          :style="{ color: labelColor }"
        >
          {{ unit.label }}
        </span>
      </div>
    </div>
  </section>
</template>
