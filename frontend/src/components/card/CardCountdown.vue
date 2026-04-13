<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';

const props = defineProps({
  targetDate: { type: String, required: true },
  themeColor: { type: String, default: '#4f46e5' },
  templateId: { type: String, default: 'modern-chic' }
});

const timeLeft = ref({ days: 0, hours: 0, minutes: 0, seconds: 0 });
const isExpired = ref(false);
let timer = null;

const calculateTimeLeft = () => {
  const difference = +new Date(props.targetDate) - +new Date();
  if (difference > 0) {
    timeLeft.value = {
      days: Math.floor(difference / (1000 * 60 * 60 * 24)),
      hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((difference / 1000 / 60) % 60),
      seconds: Math.floor((difference / 1000) % 60)
    };
  } else {
    isExpired.value = true;
    if (timer) clearInterval(timer);
  }
};

onMounted(() => {
  calculateTimeLeft();
  timer = setInterval(calculateTimeLeft, 1000);
});

onUnmounted(() => { if (timer) clearInterval(timer); });

const containerClass = computed(() => `countdown-${props.templateId}`);
</script>

<template>
  <div :class="['flex justify-center items-center gap-4 md:gap-8', containerClass]">
    <template v-if="!isExpired">
      <div v-for="(val, unit) in { Jours: timeLeft.days, Heures: timeLeft.hours, Min: timeLeft.minutes, Sec: timeLeft.seconds }" :key="unit" 
           class="flex flex-col items-center group">
        <div class="number-box relative flex items-center justify-center">
           <span class="text-3xl md:text-5xl font-bold transition-all group-hover:scale-110" :style="{ color: themeColor }">{{ val }}</span>
        </div>
        <span class="text-[10px] md:text-xs uppercase tracking-[0.2em] font-bold mt-2 opacity-60">{{ unit }}</span>
      </div>
    </template>
    <div v-else class="text-2xl font-serif italic text-center p-4" :style="{ color: themeColor }">
      C'est le grand jour ! ✨
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.number-box {
  min-width: 60px;
}

/* Style spécifique Rose Romantique */
.countdown-romantic-pink .number-box {
  @apply bg-rose-50 rounded-full w-16 h-16 shadow-inner border border-rose-100;
}
@media (min-width: 768px) {
  .countdown-romantic-pink .number-box {
    @apply w-24 h-24;
  }
}

/* Style spécifique Luxe Minimaliste */
.countdown-luxury-minimal .number-box {
  @apply border-b-2 border-black rounded-none w-14 h-14;
}
@media (min-width: 768px) {
  .countdown-luxury-minimal .number-box {
    @apply w-20 h-20;
  }
}
.countdown-luxury-minimal span {
  font-family: 'Montserrat', sans-serif;
  @apply tracking-tighter;
}

/* Style spécifique Élégance Classique */
.countdown-classic-elegance .number-box {
  @apply bg-stone-50 border border-stone-200 rounded-lg shadow-sm w-16 h-16;
}
@media (min-width: 768px) {
  .countdown-classic-elegance .number-box {
    @apply w-24 h-24;
  }
}
</style>
