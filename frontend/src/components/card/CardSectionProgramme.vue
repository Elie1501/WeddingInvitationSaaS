<script setup>
// CardSectionProgramme.vue — Phase 2
// Section partagée. Lecture directe config/event (même convention que RSVP).
// Aucune logique : juste l'affichage de la liste des sous-événements.
import { computed, inject } from 'vue';

const props = defineProps({
  config:    { type: Object, required: true },
  event:     { type: Object, required: true },
  subEvents: { type: Array, default: null }, // prioritaire : prop directe depuis CardRenderer
});

// En mode éditeur, on affiche toujours le bloc (même vide) pour qu'il soit visible
// et éditable ; en vue publique on masque un programme vide.
const isEditorMode = inject('isEditorMode', false);

const theme   = computed(() => props.config.theme   || {});
const content = computed(() => props.config.content || {});

const labelColor = computed(() => (theme.value.text || '#1A1A1A') + 'B3');

// Si la prop subEvents est fournie (cas CardRenderer), elle prime sur config/event.
const items = computed(() => {
  if (props.subEvents?.length) return props.subEvents;
  return props.config.sub_events || content.value.sub_events || props.event.sub_events || [];
});
</script>

<template>
  <!-- Public : masqué si vide. Éditeur : toujours visible (état vide éditable). -->
  <section
    v-if="items.length || isEditorMode"
    class="programme-section py-16 px-6 max-w-xl mx-auto transition-all duration-700"
    :style="{ fontFamily: theme.fontFamily }"
  >
    <h2
      class="text-center italic mb-10"
      style="font-size: var(--size-headings, clamp(1.75rem, 7vw, 2.25rem)); overflow-wrap: break-word"
      :style="{ color: `var(--color-section-title, ${theme.text || '#1A1A1A'})`, fontFamily: theme.fontFamily }"
    >
      {{ content.programme_title || 'Le Programme' }}
    </h2>

    <ul class="space-y-8">
      <li
        v-for="(item, idx) in items"
        :key="idx"
        class="flex flex-col items-center text-center"
      >
        <!-- Heure -->
        <span
          v-if="item.time"
          class="uppercase tracking-[0.2em] mb-1"
          style="font-size: var(--size-label, 0.7rem)"
          :style="{ color: `var(--color-countdown, ${theme.accent || theme.text || '#1A1A1A'})` }"
        >
          {{ item.time }}
        </span>

        <!-- Intitulé -->
        <h3
          class="font-medium"
          style="font-size: var(--size-body, clamp(1rem, 4.5vw, 1.25rem)); overflow-wrap: break-word; max-width: 100%"
          :style="{ color: theme.text || '#1A1A1A' }"
        >
          {{ item.title || item.name }}
        </h3>

        <!-- Lieu -->
        <p
          v-if="item.location"
          class="mt-1"
          style="font-size: var(--size-body, 0.875rem); overflow-wrap: break-word; max-width: 100%"
          :style="{ color: labelColor }"
        >
          {{ item.location }}
        </p>

        <!-- Description -->
        <p
          v-if="item.description"
          class="mt-2 italic leading-relaxed"
          style="font-size: var(--size-body, 0.875rem); overflow-wrap: break-word; max-width: 32ch"
          :style="{ color: labelColor }"
        >
          {{ item.description }}
        </p>
      </li>
    </ul>

    <!-- État vide visible uniquement dans l'éditeur -->
    <p
      v-if="!items.length && isEditorMode"
      class="text-center italic opacity-50 mt-2"
      style="font-size: var(--size-body, 0.95rem)"
      :style="{ color: theme.text || '#1A1A1A' }"
    >
      Aucune étape pour l'instant — ajoutez votre programme ici.
    </p>
  </section>
</template>
