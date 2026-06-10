<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import CardRenderer from './card/CardRenderer.vue';
import { getThumbConfig, DEMO_EVENT } from '../data/demoConfigs.js';

const props = defineProps({
  templateId: { type: String, required: true },
  name:       { type: String, required: true },
  isPremium:  { type: Boolean, default: false },
});

const router  = useRouter();
const mounted = ref(false);   // lazy-mount flag
const scale   = ref(1);
const outerEl = ref(null);

// Largeur de rendu interne : 400 px (largeur téléphone typique)
const INNER_W = 400;

const config = getThumbConfig(props.templateId);
const event  = DEMO_EVENT;

let io = null;
let ro = null;

onMounted(() => {
  // IntersectionObserver : ne monte le composant que quand la carte approche du viewport
  io = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) { mounted.value = true; io.disconnect(); } },
    { rootMargin: '300px' }
  );
  io.observe(outerEl.value);

  // ResizeObserver : recalcule le scale quand la colonne change de taille
  ro = new ResizeObserver(([entry]) => {
    scale.value = entry.contentRect.width / INNER_W;
  });
  ro.observe(outerEl.value);
});

onUnmounted(() => {
  io?.disconnect();
  ro?.disconnect();
});

const handleClick = () => router.push(`/demo/${props.templateId}`);
</script>

<template>
  <div class="group cursor-pointer" @click="handleClick">

    <!-- Cadre portrait (ratio 3:4, comme une vraie invitation) -->
    <div ref="outerEl"
         class="relative aspect-[3/4] overflow-hidden rounded-2xl bg-neutral-100 shadow-md
                group-hover:shadow-xl transition-shadow duration-500">

      <!-- Rendu réel du template, réduit par scale -->
      <div v-if="mounted && config"
           class="absolute top-0 left-0 pointer-events-none"
           :style="{
             width:           INNER_W + 'px',
             transformOrigin: 'top left',
             transform:       `scale(${scale})`,
           }">
        <CardRenderer
          :config="config"
          :event="event"
          :subEvents="[]"
          :selectedBlock="null"
        />
      </div>

      <!-- Placeholder animé tant que non monté -->
      <div v-else class="absolute inset-0 bg-neutral-200 animate-pulse" />

      <!-- Overlay au hover + bouton "Voir le template" -->
      <div class="absolute inset-0 flex items-center justify-center
                  bg-black/0 group-hover:bg-black/25 transition-colors duration-500">
        <span class="opacity-0 group-hover:opacity-100
                     transition-all duration-300 delay-75
                     translate-y-2 group-hover:translate-y-0
                     px-5 py-3 bg-white text-neutral-900 text-[10px] font-bold
                     uppercase tracking-[0.25em] rounded-xl shadow-lg">
          Voir le template
        </span>
      </div>

      <!-- Badge Premium -->
      <div v-if="isPremium" class="absolute top-3 right-3 z-10">
        <span class="text-[9px] font-bold uppercase tracking-widest px-3 py-1.5
                     rounded-full bg-primary-500 text-white shadow-sm">
          Premium
        </span>
      </div>

    </div>

    <!-- Nom sous la carte -->
    <div class="mt-3 px-1">
      <h3 class="font-serif italic text-neutral-900 text-base">{{ name }}</h3>
    </div>

  </div>
</template>
