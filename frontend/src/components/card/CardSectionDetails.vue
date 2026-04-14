<script setup>
defineProps(['section', 'event', 'config']);
</script>

<template>
  <div class="p-10 bg-transparent grid grid-cols-1 md:grid-cols-2 gap-8 border-t border-gray-50">
    <div class="flex flex-col items-center p-6 rounded-2xl bg-gray-50 shadow-sm" :style="{ borderTop: `4px solid ${config?.colors?.accent || '#E5E7EB'}` }">
       <span class="text-xs uppercase tracking-wider text-gray-400 mb-1">Date</span>
       <span class="text-gray-900 font-medium font-sans">
          {{ new Date(event.date).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
       </span>
    </div>
    <div class="flex flex-col items-center p-6 rounded-2xl bg-gray-50 shadow-sm" :style="{ borderTop: `4px solid ${config?.colors?.accent || '#E5E7EB'}` }">
       <span class="text-xs uppercase tracking-wider text-gray-400 mb-1">Lieu</span>
       <span class="text-gray-900 font-medium font-sans">{{ event.location }}</span>
    </div>
  </div>
</template>
