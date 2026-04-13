<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';
import CardSplashScreen from '../components/card/CardSplashScreen.vue';

const route = useRoute();
const slug = route.params.slug;
const cardData = ref(null);
const loading = ref(true);
const error = ref('');
const successMessage = ref('');

const rsvpForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  presence: true,
  plus_ones: 0,
  dietary_restrictions: '',
  message: ''
});

const isMusicPlaying = ref(false);
const audioPlayer = ref(null);
const showSplashFallback = ref(false);

const startMusic = () => {
  if (audioPlayer.value && !isMusicPlaying.value) {
    audioPlayer.value.play().then(() => {
      isMusicPlaying.value = true;
    }).catch(e => console.log("L'audio a été bloqué par le navigateur", e));
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
    }).catch(e => console.log("L'audio a été bloqué", e));
  }
};

onMounted(async () => {
  try {
    const response = await api.get(`/events/public/card/${slug}`);
    cardData.value = response.data;
    
    // Initialiser le splash screen si activé
    const config = JSON.parse(cardData.value.config_json || '{}');
    if (config.has_cover_page) {
      showSplashFallback.value = true;
    }
  } catch (err) {
    error.value = "Invitation introuvable ou non publiée.";
    console.error(err);
  } finally {
    loading.value = false;
  }
});

const handleRSVP = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    await api.post('/guests/public/rsvp', {
      ...rsvpForm.value,
      event_id: cardData.value.event_id || cardData.value.id
    });
    
    successMessage.value = "Merci ! Votre réponse a bien été enregistrée.";
    rsvpForm.value = { first_name: '', last_name: '', email: '', presence: true, plus_ones: 0, dietary_restrictions: '', message: '' };
  } catch (err) {
    error.value = "Une erreur est survenue lors de l'enregistrement de votre réponse.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-primary-50 py-12 px-4 flex flex-col items-center font-sans">
    
    <!-- Floating Music Control -->
    <div v-if="cardData?.music_url" class="fixed bottom-8 right-8 z-[300]">
      <button 
        @click="toggleMusic"
        class="w-14 h-14 bg-white rounded-full shadow-2xl flex items-center justify-center text-primary-600 hover:scale-110 transition-all border border-primary-100 group relative"
      >
        <div v-if="isMusicPlaying" class="flex items-end space-x-1 h-6">
          <div class="w-1 bg-primary-500 bar-1"></div>
          <div class="w-1 bg-primary-600 bar-2"></div>
          <div class="w-1 bg-primary-500 bar-3"></div>
        </div>
        <svg v-else class="w-6 h-6 ml-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
        
        <!-- Tooltip -->
        <span class="absolute right-16 bg-gray-900 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none shadow-xl">
          {{ isMusicPlaying ? 'Couper la musique' : 'Écouter la musique' }}
        </span>
      </button>
      <audio ref="audioPlayer" loop :src="cardData.music_url" class="hidden"></audio>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !cardData" class="flex items-center justify-center py-20">
       <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error && !cardData" class="text-center py-20">
      <h1 class="text-3xl font-serif text-gray-900 mb-4 italic">Oups !</h1>
      <p class="text-gray-500 font-sans">{{ error }}</p>
      <router-link to="/" class="mt-8 inline-block text-primary-600 font-sans hover:underline">Retourner à l'accueil</router-link>
    </div>

    <!-- Invitation View -->
    <div v-if="cardData" class="w-full max-w-2xl bg-white rounded-3xl shadow-2xl overflow-hidden shadow-primary-900/10 border border-primary-100 flex flex-col">
      
      <!-- Content: CardRenderer handles its own splash screen state internally -->
      <CardRenderer 
        :config="{ ...JSON.parse(cardData.config_json || '{}'), itinerary: cardData.sub_events }" 
        :event="cardData.event || { groom_name: cardData.groom_name, bride_name: cardData.bride_name, date: cardData.date, location: cardData.location, title: cardData.title }" 
        :templateId="cardData.template_id || 'modern-chic'"
        :isEditor="false"
        @play-music="startMusic"
      />

      <!-- RSVP Form (Integrated into the main container) -->
      <div v-if="cardData.has_rsvp_form" 
           class="p-10 md:p-16 border-t border-primary-50"
           :style="{ backgroundColor: (JSON.parse(cardData.config_json || '{}').colors?.background || '#ffffff') }">
        <div class="text-center mb-10">
          <h3 class="text-3xl font-serif text-primary-900 mb-2">
            {{ JSON.parse(cardData.config_json || '{}').content?.rsvp_title || 'Confirmez votre présence' }}
          </h3>
          <p class="text-gray-500 font-sans">
            {{ JSON.parse(cardData.config_json || '{}').content?.rsvp_subtitle || 'Veuillez nous donner une réponse avant la date limite.' }}
          </p>
        </div>

        <div v-if="successMessage" class="bg-secondary-50 border border-secondary-200 text-secondary-800 p-6 rounded-2xl text-center font-sans mb-8">
           {{ successMessage }}
        </div>

        <form v-else @submit.prevent="handleRSVP" class="space-y-6">
          <div class="flex justify-center space-x-4 mb-8">
            <button type="button" @click="rsvpForm.presence = true" :class="rsvpForm.presence ? 'bg-green-600 text-white shadow-lg' : 'bg-gray-100 text-gray-500'" class="px-6 py-2 rounded-xl text-sm font-bold transition-all">PRÉSENT(E)</button>
            <button type="button" @click="rsvpForm.presence = false" :class="!rsvpForm.presence ? 'bg-red-600 text-white shadow-lg' : 'bg-gray-100 text-gray-500'" class="px-6 py-2 rounded-xl text-sm font-bold transition-all">ABSENT(E)</button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input v-model="rsvpForm.first_name" type="text" placeholder="Prénom" required class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all" />
            <input v-model="rsvpForm.last_name" type="text" placeholder="Nom" required class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all" />
          </div>
          
          <input v-if="JSON.parse(cardData.config_json || '{}').rsvp?.ask_email !== false" v-model="rsvpForm.email" type="email" placeholder="Email (facultatif)" class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all" />

          <div v-if="rsvpForm.presence && JSON.parse(cardData.config_json || '{}').rsvp?.ask_plus_ones !== false" class="space-y-2">
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">Nombre d'accompagnants</label>
            <input v-model.number="rsvpForm.plus_ones" type="number" min="0" class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all" />
          </div>

          <div v-if="rsvpForm.presence && JSON.parse(cardData.config_json || '{}').rsvp?.ask_dietary !== false">
            <input v-model="rsvpForm.dietary_restrictions" type="text" placeholder="Restrictions alimentaires (facultatif)" class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all" />
          </div>

          <div v-if="JSON.parse(cardData.config_json || '{}').rsvp?.ask_message !== false">
            <textarea v-model="rsvpForm.message" rows="3" placeholder="Un petit message pour les mariés ?" class="w-full px-4 py-3 rounded-xl border border-primary-100 bg-primary-50/20 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all"></textarea>
          </div>

          <button type="submit" :disabled="loading" class="w-full py-4 text-white rounded-xl font-semibold shadow-lg shadow-primary-900/10 hover:shadow-primary-900/20 transition-all transform active:scale-[0.98]" :style="{ backgroundColor: rsvpForm.presence ? (cardData.theme_color || '#4f46e5') : '#dc2626' }">
            {{ loading ? 'Envoi...' : 'Envoyer ma réponse' }}
          </button>
        </form>
      </div>
    </div>

    <p class="mt-12 text-gray-400 text-xs font-sans uppercase tracking-widest italic opacity-50">
      Fait avec amour sur Saas Wedding
    </p>
  </div>
</template>

<style scoped>
.bar-1 { animation: music 0.8s ease-in-out infinite; }
.bar-2 { animation: music 0.8s ease-in-out 0.2s infinite; }
.bar-3 { animation: music 0.8s ease-in-out 0.4s infinite; }

@keyframes music {
  0%, 100% { height: 8px; }
  50% { height: 20px; }
}
</style>
