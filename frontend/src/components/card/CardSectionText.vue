<script setup>
import { computed } from 'vue';
const props = defineProps(['id', 'section', 'event', 'config']);

const contentData = computed(() => {
    if (props.id && props.config?.content?.[props.id]) {
        return props.config.content[props.id];
    }
    return {
        title: props.config?.content?.custom_text_title || '',
        content: props.config?.content?.custom_text_content || 'Nous serions honorés de votre présence pour célébrer notre union...'
    };
});

const title = computed(() => contentData.value.title);
const content = computed(() => contentData.value.content);
</script>

<template>
  <div class="py-16 px-8 text-center bg-transparent reveal-up">
    <h2 v-if="title" class="text-4xl md:text-5xl mb-8 font-playfair italic">
      {{ title }}
    </h2>
    
    <div 
      class="text-content text-lg md:text-xl leading-relaxed max-w-2xl mx-auto font-light tracking-wide whitespace-pre-line opacity-80"
    >
      {{ content }}
    </div>

    <div class="w-12 h-[1px] mx-auto mt-12 bg-current opacity-20"></div>
  </div>
</template>

<style scoped>
.reveal-up {
  animation: fadeInUp 1s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
