<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';
import CardSplashScreen from '../components/card/CardSplashScreen.vue';

const route = useRoute();
const router = useRouter();
const slug = route.params.slug;
const cardData = ref(null);
const loading = ref(true);
const error = ref('');
const successMessage = ref('');

const showSplash = ref(false);
const config = computed(() => {
  if (!cardData.value?.config_json) return {};
  try {
    return JSON.parse(cardData.value.config_json);
  } catch (e) {
    return {};
  }
});

watch(cardData, (newVal) => {
  if (newVal) {
    const cfg = JSON.parse(newVal.config_json || '{}');
    if (cfg.show_splash) {
      showSplash.value = true;
    }
  }
});

const rsvpForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  presence: true,
  plus_ones: 0,
  sub_guests: [],
  dietary_restrictions: '',
  message: ''
});

watch(() => rsvpForm.value.plus_ones, (newVal) => {
  const currentLen = rsvpForm.value.sub_guests.length;
  if (newVal > currentLen) {
    for (let i = 0; i < newVal - currentLen; i++) {
      rsvpForm.value.sub_guests.push({ first_name: '', last_name: '', dietary_restrictions: '' });
    }
  } else if (newVal < currentLen) {
    rsvpForm.value.sub_guests = rsvpForm.value.sub_guests.slice(0, newVal);
  }
});

const isMusicPlaying = ref(false);
const audioPlayer = ref(null);

const startMusic = () => {
  if (audioPlayer.value && !isMusicPlaying.value) {
    audioPlayer.value.play().then(() => {
      isMusicPlaying.value = true;
    }).catch(e => console.log("Audio bloqué", e));
  }
};

const toggleMusic = () => {
  if (!audioPlayer.value) return;
  if (isMusicPlaying.value) {
    audioPlayer.value.pause();
    isMusicPlaying.value = false;
  } else {
    audioPlayer.value.play().then(() => {
      isMusicPlaying.value = true;
    }).catch(e => console.log("Audio bloqué", e));
  }
};

onMounted(async () => {
  try {
    const response = await api.get(`/events/public/card/${slug}`);
    cardData.value = response.data;
  } catch (err) {
    error.value = "Invitation introuvable.";
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="min-h-screen bg-[#FDFCFB] flex flex-col items-center selection:bg-[#C5A059] selection:text-white font-serif">
    
    <!-- Splash Screen Overlay -->
    <CardSplashScreen 
      v-if="showSplash && cardData" 
      :config="config" 
      :event="cardData.event || cardData" 
      :template-id="cardData.template_id"
      @close="showSplash = false"
      @play-music="startMusic"
    />

    <!-- Musique -->
    <div v-if="cardData?.music_url" class="fixed bottom-8 right-8 z-[300]">
      <button @click="toggleMusic" class="w-12 h-12 bg-white border border-gray-100 rounded-full shadow-lg flex items-center justify-center text-[#1A1A1A] hover:scale-110 transition-all">
        <div v-if="isMusicPlaying" class="flex items-end space-x-1 h-4">
          <div class="w-[2px] bg-[#C5A059] animate-music-bar-1"></div>
          <div class="w-[2px] bg-[#C5A059] animate-music-bar-2"></div>
          <div class="w-[2px] bg-[#C5A059] animate-music-bar-3"></div>
        </div>
        <svg v-else class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
      </button>
      <audio ref="audioPlayer" loop :src="cardData.music_url" class="hidden"></audio>
    </div>

    <!-- Bouton Édition (Propriétaire uniquement) -->
    <div v-if="cardData?.is_owner" class="fixed bottom-8 left-8 z-[300]">
      <button @click="router.push(`/editor/${cardData.card_id}`)" class="px-6 py-3 bg-[#1A1A1A] text-white rounded-full shadow-2xl flex items-center space-x-3 hover:scale-105 transition-all group">
        <svg class="w-4 h-4 group-hover:rotate-12 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
        </svg>
        <span class="text-xs font-bold uppercase tracking-widest">Modifier mon invitation</span>
      </button>
    </div>

    <div v-if="cardData" class="w-full flex flex-col items-center">
      
      <!-- Carte -->
      <div class="w-full max-w-[500px] bg-white shadow-2xl overflow-hidden mb-20 md:mt-10 md:rounded-[40px] md:border-[12px] md:border-[#1A1A1A]">
        <CardRenderer 
          :config="JSON.parse(cardData.config_json || '{}')" 
          :event="cardData.event || cardData" 
          :sub-events="cardData.sub_events"
          @play-music="startMusic"
        />
      </div>

      <footer class="py-20 text-center opacity-20">
        <p class="text-[9px] uppercase tracking-[0.5em]">Saas Wedding • 2026</p>
      </footer>

    </div>
  </div>
</template>

<style scoped>
@keyframes music-bar { 0%, 100% { height: 4px; } 50% { height: 16px; } }
.animate-music-bar-1 { animation: music-bar 0.6s ease-in-out infinite; }
.animate-music-bar-2 { animation: music-bar 0.6s ease-in-out 0.2s infinite; }
.animate-music-bar-3 { animation: music-bar 0.6s ease-in-out 0.4s infinite; }
@keyframes fade-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
</style>
