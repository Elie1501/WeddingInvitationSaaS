<script setup>
import { computed } from 'vue';

const props = defineProps({
  layout: { type: String, default: 'arch' },
  theme: { type: Object, required: true },
  displayData: { type: Object, required: true }
});
</script>

<template>
  <div class="hero-block relative w-full aspect-[9/16] overflow-hidden shadow-2xl" :style="{ backgroundColor: theme.background, color: theme.text }">
    
    <!-- STYLE : L'ARCHE -->
    <div v-if="layout === 'arch'" class="h-full flex flex-col items-center p-8 text-center relative justify-end">
      <div class="absolute top-12 w-[80%] aspect-[1/1.4] overflow-hidden shadow-2xl" style="border-radius: 1000px 1000px 0 0; border: 4px solid white;">
        <img :src="displayData.image" class="w-full h-full object-cover" />
      </div>
      <div class="relative z-10 w-full flex flex-col items-center bg-gradient-to-t from-[var(--bg-color)] via-[var(--bg-color)] to-transparent pt-32 pb-8 px-4" :style="{'--bg-color': theme.background}">
        <p class="text-[10px] uppercase tracking-[0.4em] mb-4" :style="{ color: theme.accent }">Save the Date</p>
        <h1 class="text-6xl font-light leading-none italic mb-8 drop-shadow-sm">{{ displayData.names }}</h1>
        <div class="w-12 h-[1px] mx-auto opacity-30 mb-6" :style="{ backgroundColor: theme.text }"></div>
        <p class="text-sm tracking-widest font-bold uppercase mb-1">{{ displayData.date }}</p>
        <p class="text-[10px] uppercase tracking-widest opacity-60">{{ displayData.location }}</p>
      </div>
    </div>

    <!-- STYLE : EDITORIAL -->
    <div v-else-if="layout === 'typography-focus'" class="h-full flex flex-col p-10 relative overflow-hidden text-left justify-between">
      <div class="absolute top-10 left-10 w-3/4 aspect-[4/5] overflow-hidden shadow-xl rounded-2xl opacity-90">
        <img :src="displayData.image" class="w-full h-full object-cover grayscale mix-blend-multiply" />
      </div>
      <div class="relative z-10 flex flex-col h-full justify-end pb-8 pt-48">
        <h1 class="text-[5.5rem] font-black tracking-tighter uppercase leading-[0.85] w-[120%] -ml-2 mix-blend-difference break-words">{{ displayData.names.replace(' & ', '&') }}</h1>
        <div class="mt-12 flex justify-between items-end border-t-2 pt-6" :style="{ borderColor: theme.text }">
          <div class="space-y-1">
            <p class="text-xs tracking-widest uppercase font-bold">{{ displayData.date }}</p>
            <p class="text-[9px] uppercase tracking-widest opacity-60">{{ displayData.location }}</p>
          </div>
          <div class="w-10 h-10 rounded-full border-2 flex items-center justify-center flex-shrink-0" :style="{ borderColor: theme.text }">
            <span class="text-[8px] font-bold">OUI</span>
          </div>
        </div>
      </div>
    </div>

    <!-- STYLE : SPLIT -->
    <div v-else-if="layout === 'split'" class="h-full w-full relative flex items-center justify-center p-8">
      <div class="absolute inset-0">
        <img :src="displayData.image" class="w-full h-full object-cover" />
        <div class="absolute inset-0 bg-black/20"></div>
      </div>
      <div class="relative z-10 w-full max-w-[90%] bg-white/20 backdrop-blur-xl border border-white/40 p-12 rounded-[2.5rem] text-center flex flex-col items-center space-y-8 shadow-2xl text-white">
        <p class="text-[9px] uppercase tracking-[0.4em] opacity-90 font-bold">Nous nous marions</p>
        <h1 class="text-5xl italic font-light drop-shadow-md leading-tight">{{ displayData.names }}</h1>
        <div class="w-12 h-[2px] bg-white/50 mx-auto"></div>
        <div class="space-y-3 pt-2">
          <p class="text-sm font-bold tracking-[0.2em] uppercase drop-shadow-sm">{{ displayData.date }}</p>
          <p class="text-[10px] uppercase tracking-widest opacity-80 font-medium">{{ displayData.location }}</p>
        </div>
      </div>
    </div>

    <!-- STYLE : ORA (FULL HERO) -->
    <div v-else-if="layout === 'ora'" class="h-full w-full flex flex-col justify-end bg-center bg-cover" :style="{ backgroundImage: `url(${displayData.image})` }">
       <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[var(--bg-light)]" :style="{'--bg-light': theme.background}"></div>
       <div class="relative z-10 p-12 text-center">
          <h1 class="main-names text-6xl italic font-light mb-4 drop-shadow-lg">{{ displayData.names }}</h1>
          <div class="w-12 h-[1px] bg-[#C5A059] mx-auto mb-8"></div>
       </div>
    </div>

    <!-- STYLE : ES (LUXE MINIMAL) -->
    <div v-else-if="layout === 'es'" class="h-full w-full flex flex-col items-center justify-center p-12 text-center relative bg-white">
      <div class="absolute inset-0 opacity-10">
        <img :src="displayData.image" class="w-full h-full object-cover grayscale" />
      </div>
      <div class="relative z-10 border-2 border-black p-10 bg-white/90 backdrop-blur-sm">
        <p class="text-[10px] font-black uppercase tracking-[0.5em] mb-6 text-black">ES</p>
        <h1 class="text-5xl font-black uppercase tracking-tighter leading-none mb-8 text-black">{{ displayData.names }}</h1>
        <div class="w-8 h-[4px] bg-black mx-auto mb-8"></div>
        <p class="text-xs font-bold tracking-[0.3em] uppercase text-black">{{ displayData.date }}</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
.main-names { animation: fadeInUp 1.2s ease-out; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
