<script setup>
defineProps(['section', 'event', 'config']);
</script>

<template>
  <div class="p-10 text-center bg-white">
    <h2 class="text-2xl font-serif mb-6 italic" :style="{ color: config?.colors?.text || '#1f2937', fontFamily: config?.typography?.headings || 'serif' }">
      {{ event.title }}
    </h2>
    <p class="text-gray-600 leading-relaxed max-w-md mx-auto" :style="{ color: config?.colors?.text_muted || '#4b5563' }">
      {{ section?.content || config?.content?.intro_text || 'Nous serions honorés de votre présence pour célébrer notre union...' }}
    </p>
  </div>
</template>
