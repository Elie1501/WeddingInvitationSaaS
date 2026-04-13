<script setup>
import { computed } from 'vue';
const props = defineProps(['section', 'event', 'config']);

const accentColor = computed(() => props.config?.colors?.accent || '#4f46e5');
const textColor = computed(() => props.config?.colors?.text || '#1f2937');

const getMapsUrl = (location) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location)}`;
</script>

<template>
  <div class="p-10 md:p-16 border-b border-gray-50/50" :style="{ backgroundColor: config?.background_color || 'transparent' }">
    <h2 class="text-3xl font-serif text-center mb-16 italic" :style="{ color: accentColor }">Programme de la journée</h2>
    
    <div class="relative max-w-2xl mx-auto">
      <!-- Ligne centrale verticale (MD) -->
      <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-100 md:left-1/2 md:-ml-px opacity-50"></div>
      
      <div class="space-y-16">
        <div v-for="(item, index) in config.itinerary" :key="index" class="relative flex items-start md:flex-row flex-col">
          
          <!-- Dot -->
          <div class="absolute left-4 w-4 h-4 rounded-full border-4 border-white shadow-md mt-1.5 -ml-2 z-10 md:left-1/2 md:ml-[-8px] transition-transform hover:scale-125" :style="{ backgroundColor: accentColor }"></div>
          
          <!-- Content Left (Even index on MD) -->
          <div :class="index % 2 === 0 ? 'md:text-right md:pr-16 order-2 md:order-1' : 'md:opacity-0 md:pointer-events-none order-2 md:order-1'" class="pl-12 md:pl-0 w-full md:w-1/2 mt-4 md:mt-0">
             <template v-if="index % 2 === 0 || true">
                <div class="inline-block px-4 py-1 rounded-full text-[10px] font-bold uppercase tracking-[0.2em] mb-3 shadow-sm bg-white border border-gray-100" :style="{ color: accentColor }">
                  {{ item.time }}
                </div>
                <h3 class="text-xl font-bold mb-2" :style="{ color: textColor }">{{ item.title }}</h3>
                
                <a v-if="item.location" :href="getMapsUrl(item.location)" target="_blank" class="inline-flex items-center text-[11px] font-bold uppercase tracking-widest mb-3 hover:underline group" :style="{ color: accentColor }">
                  <svg class="w-3.5 h-3.5 mr-1.5 transition-transform group-hover:bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
                  {{ item.location }}
                </a>
                
                <p class="text-sm leading-relaxed opacity-70 italic whitespace-pre-line" :style="{ color: textColor }">{{ item.description }}</p>
             </template>
          </div>
          
          <!-- Spacer for MD -->
          <div class="hidden md:block md:w-1/2 order-2"></div>

          <!-- Re-render content for Odd index on MD (positioned right) -->
          <div v-if="index % 2 !== 0" class="hidden md:block absolute left-1/2 w-1/2 pl-16 text-left">
                <div class="inline-block px-4 py-1 rounded-full text-[10px] font-bold uppercase tracking-[0.2em] mb-3 shadow-sm bg-white border border-gray-100" :style="{ color: accentColor }">
                  {{ item.time }}
                </div>
                <h3 class="text-xl font-bold mb-2" :style="{ color: textColor }">{{ item.title }}</h3>
                
                <a v-if="item.location" :href="getMapsUrl(item.location)" target="_blank" class="inline-flex items-center text-[11px] font-bold uppercase tracking-widest mb-3 hover:underline group" :style="{ color: accentColor }">
                  <svg class="w-3.5 h-3.5 mr-1.5 transition-transform group-hover:bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
                  {{ item.location }}
                </a>
                
                <p class="text-sm leading-relaxed opacity-70 italic whitespace-pre-line" :style="{ color: textColor }">{{ item.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
.group-hover\:bounce {
  animation: bounce 1s ease infinite;
}
</style>
