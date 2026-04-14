<script setup>
import { computed } from 'vue';

const props = defineProps({
  element: {
    type: Object,
    required: true
  },
  event: {
    type: Object,
    default: () => ({})
  },
  isSelected: {
    type: Boolean,
    default: false
  }
});

const processedContent = computed(() => {
  if (props.element.type !== 'text') return props.element.content;
  
  let content = props.element.content || '';
  // Injection dynamique des variables de l'événement
  content = content.replace('{groom_name}', props.event.groom_name || 'Marié 1');
  content = content.replace('{bride_name}', props.event.bride_name || 'Marié 2');
  content = content.replace('{location}', props.event.location || 'Lieu de l\'événement');
  
  if (props.event.date) {
    const dateStr = new Date(props.event.date).toLocaleDateString('fr-FR', { 
      day: 'numeric', month: 'long', year: 'numeric' 
    });
    content = content.replace('{date}', dateStr);
  }
  
  return content;
});

const elementStyle = computed(() => {
  const s = props.element.style || {};
  return {
    position: 'absolute',
    top: `${props.element.y}px`,
    left: `${props.element.x}px`,
    width: `${props.element.width}px`,
    height: `${props.element.height}px`,
    zIndex: props.element.zIndex || 1,
    ...s,
    // On s'assure que fontSize est bien en px si c'est un nombre
    fontSize: typeof s.fontSize === 'number' ? `${s.fontSize}px` : s.fontSize,
    // Gestion du curseur pour l'éditeur
    cursor: 'pointer',
    // Contour si sélectionné
    outline: props.isSelected ? '2px solid #6366f1' : 'none',
    outlineOffset: '2px'
  };
});
</script>

<template>
  <div :style="elementStyle" class="canvas-element transition-all duration-300">
    <!-- TEXT ELEMENT -->
    <div v-if="element.type === 'text'" class="w-full h-full whitespace-pre-line overflow-hidden">
      {{ processedContent }}
    </div>

    <!-- IMAGE ELEMENT -->
    <img v-else-if="element.type === 'image'" :src="processedContent" class="w-full h-full object-cover" />

    <!-- SHAPE ELEMENT -->
    <div v-else-if="element.type === 'shape'" class="w-full h-full"></div>
  </div>
</template>

<style scoped>
.canvas-element:hover {
  outline: 1px dashed rgba(99, 102, 241, 0.5);
  outline-offset: 2px;
}
</style>
