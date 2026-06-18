<script setup>
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CardRenderer from '../components/card/CardRenderer.vue';
import { DEMO_CONFIGS, DEMO_EVENT } from '../data/demoConfigs.js';

const route  = useRoute();
const router = useRouter();
const slug   = route.params.slug;

const config       = computed(() => DEMO_CONFIGS[slug] ?? DEMO_CONFIGS['riviera-blanche']);
const templateName = computed(() => config.value?.name ?? slug);

onMounted(() => { window.scrollTo(0, 0); });

const goRegister = () => router.push({ path: '/register', query: { template: slug } });
</script>

<template>
  <div class="relative min-h-screen bg-neutral-50">

    <!-- Bandeau "mode démo" discret en haut -->
    <div class="fixed top-0 inset-x-0 z-50 flex items-center justify-between
                px-4 sm:px-6 py-2.5 bg-white/90 backdrop-blur-sm border-b border-primary-100
                text-[10px] font-bold uppercase tracking-[0.2em]">
      <router-link to="/"
                   class="flex items-center gap-2 text-neutral-400 hover:text-neutral-900 transition-colors">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/>
        </svg>
        Retour
      </router-link>
      <span class="text-neutral-400">
        Aperçu · <span class="text-primary-500">{{ templateName }}</span>
      </span>
      <span class="text-neutral-300 hidden sm:block">Données fictives</span>
    </div>

    <!-- Rendu de la carte centrée, même style que la vue publique -->
    <div class="pt-12 pb-24 flex justify-center">
      <div class="w-full max-w-[480px] bg-white shadow-2xl
                  md:mt-8 md:rounded-[36px] md:border-[10px] md:border-neutral-900
                  overflow-hidden">
        <CardRenderer
          :config="config"
          :event="DEMO_EVENT"
          :subEvents="[]"
          :selectedBlock="null"
        />
      </div>
    </div>

    <!-- CTA flottant : Créer avec ce design -->
    <div class="fixed bottom-5 sm:bottom-6 left-1/2 -translate-x-1/2 z-50 w-max max-w-[92vw]">
      <button @click="goRegister"
              class="flex items-center gap-2 sm:gap-3 px-5 sm:px-7 py-3 sm:py-4
                     bg-neutral-900 text-white rounded-full shadow-2xl shadow-neutral-900/30
                     text-[10px] sm:text-[11px] font-bold uppercase tracking-[0.12em] sm:tracking-[0.25em]
                     whitespace-nowrap
                     hover:bg-primary-700 transition-all
                     transform hover:-translate-y-0.5 active:scale-95">
        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span class="sm:hidden">Créer avec ce design</span>
        <span class="hidden sm:inline">Créer mon invitation avec ce design</span>
      </button>
    </div>

  </div>
</template>
