<script setup>
import { computed } from 'vue';
const props = defineProps(['section', 'event', 'config']);

const images = computed(() => {
  return props.section?.images || [
    'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?auto=format&fit=crop&q=80&w=600'
  ];
});

const gridClass = computed(() => {
  const count = images.value.length;
  if (count === 1) return 'grid-cols-1';
  if (count === 2) return 'grid-cols-2';
  if (count === 3) return 'grid-cols-2 md:grid-cols-3';
  return 'grid-cols-2 md:grid-cols-3 lg:grid-cols-4';
});
</script>

<template>
  <div class="p-8 md:p-12 bg-transparent">
    <h3 v-if="section.title" class="text-center text-2xl font-serif mb-8 italic" :style="{ color: config?.colors?.text || '#1f2937' }">
      {{ section.title }}
    </h3>
    <div :class="['grid gap-4', gridClass]">
      <div 
        v-for="(img, idx) in images" 
        :key="idx"
        class="aspect-square overflow-hidden rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300 group"
      >
        <img 
          :src="img" 
          class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" 
          alt="Wedding Gallery Image"
        />
      </div>
    </div>
  </div>
</template>
