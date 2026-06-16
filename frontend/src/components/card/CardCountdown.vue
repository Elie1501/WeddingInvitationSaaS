<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue';

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

const startTimer = () => {
  if (timer) clearInterval(timer);
  isExpired.value = false;
  calculateTimeLeft();
  timer = setInterval(calculateTimeLeft, 1000);
};

onMounted(startTimer);

watch(() => props.targetDate, startTimer);

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
    <div v-else class="text-2xl italic text-center p-4" :style="{ color: themeColor }">
      C'est le grand jour ! ✨
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";

.number-box {
  min-width: 60px;
}

/* Style spécifique Rose Romantique */
.countdown-romantic-pink .number-box {
  background-color: #fff1f2; /* rose-50 */
  border-radius: 9999px;
  width: 4rem;
  height: 4rem;
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
  border: 1px solid #ffe4e6; /* rose-100 */
}
@media (min-width: 768px) {
  .countdown-romantic-pink .number-box {
    width: 6rem;
    height: 6rem;
  }
}

/* Style spécifique Luxe Minimaliste */
.countdown-luxury-minimal .number-box {
  border-bottom: 2px solid black;
  border-radius: 0;
  width: 3.5rem;
  height: 3.5rem;
}
@media (min-width: 768px) {
  .countdown-luxury-minimal .number-box {
    width: 5rem;
    height: 5rem;
  }
}
.countdown-luxury-minimal span {
  font-family: var(--card-font, 'Montserrat'), sans-serif;
  letter-spacing: -0.05em;
}

/* Style spécifique Élégance Classique */
.countdown-classic-elegance .number-box {
  background-color: #fafaf9; /* stone-50 */
  border: 1px solid #e7e5e4; /* stone-200 */
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  width: 4rem;
  height: 4rem;
}
@media (min-width: 768px) {
  .countdown-classic-elegance .number-box {
    width: 6rem;
    height: 6rem;
  }
}
</style>
