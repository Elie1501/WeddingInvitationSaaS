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
  <div class="min-h-screen bg-neutral-50 flex flex-col items-center font-sans selection:bg-primary-100 selection:text-primary-900">
    
    <!-- Floating Music Control -->
    <div v-if="cardData?.music_url" class="fixed bottom-8 right-8 z-[300]">
      <button 
        @click="toggleMusic"
        class="w-14 h-14 bg-white/90 backdrop-blur-md rounded-full shadow-[0_10px_30px_rgba(0,0,0,0.1)] flex items-center justify-center text-primary-600 hover:scale-110 active:scale-95 transition-all border border-white group"
      >
        <div v-if="isMusicPlaying" class="flex items-end space-x-1 h-5">
          <div class="w-[3px] bg-primary-500 animate-music-bar-1"></div>
          <div class="w-[3px] bg-primary-600 animate-music-bar-2"></div>
          <div class="w-[3px] bg-primary-400 animate-music-bar-3"></div>
        </div>
        <svg v-else class="w-6 h-6 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
        
        <span class="absolute right-16 bg-gray-900 text-white text-[10px] px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none shadow-xl uppercase tracking-widest font-bold">
          {{ isMusicPlaying ? 'Couper le son' : 'Activer le son' }}
        </span>
      </button>
      <audio ref="audioPlayer" loop :src="cardData.music_url" class="hidden"></audio>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !cardData" class="fixed inset-0 bg-white z-[2000] flex flex-col items-center justify-center">
       <div class="w-16 h-[1px] bg-primary-100 mb-8 animate-grow-width"></div>
       <div class="animate-pulse text-primary-900 font-serif italic text-xl">Chargement de l'invitation...</div>
    </div>

    <!-- Invitation View -->
    <div v-if="cardData" class="w-full flex flex-col animate-fade-in">
      
      <!-- Content -->
      <div class="w-full">
        <CardRenderer 
          :config="{ ...JSON.parse(cardData.config_json || '{}'), itinerary: cardData.sub_events }" 
          :event="cardData.event || { groom_name: cardData.groom_name, bride_name: cardData.bride_name, date: cardData.date, location: cardData.location, title: cardData.title }" 
          :templateId="cardData.template_id || 'modern-chic'"
          :isEditor="false"
          @play-music="startMusic"
        />
      </div>

      <!-- RSVP Section -->
      <div v-if="cardData.has_rsvp_form" 
           class="w-full flex justify-center py-24 px-4 bg-white border-t border-neutral-100"
           id="rsvp-section">
        <div class="w-full max-w-xl">
          <div class="text-center mb-16">
            <span class="text-[10px] uppercase tracking-[0.5em] text-primary-500 font-bold mb-4 block">Votre Réponse</span>
            <h3 class="text-4xl md:text-5xl font-serif text-neutral-900 mb-6 italic">
              {{ JSON.parse(cardData.config_json || '{}').content?.rsvp_title || 'Serez-vous des nôtres ?' }}
            </h3>
            <div class="w-12 h-[1px] bg-primary-200 mx-auto mb-6"></div>
            <p class="text-neutral-500 font-light tracking-wide text-lg">
              {{ JSON.parse(cardData.config_json || '{}').content?.rsvp_subtitle || 'Veuillez nous confirmer votre présence avant la date limite.' }}
            </p>
          </div>

          <div v-if="successMessage" class="bg-primary-50/50 border border-primary-100 text-primary-900 p-8 rounded-[2rem] text-center font-serif italic text-xl animate-scale-up">
             {{ successMessage }}
          </div>

          <form v-else @submit.prevent="handleRSVP" class="space-y-8">
            <!-- Choice Buttons -->
            <div class="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <button
                type="button"
                @click="rsvpForm.presence = true"
                :class="rsvpForm.presence ? 'bg-green-600 text-white shadow-xl scale-105 shadow-green-600/20' : 'bg-neutral-50 text-neutral-400 hover:bg-neutral-100'"
                class="flex-1 px-8 py-5 rounded-2xl text-[11px] font-bold uppercase tracking-[0.2em] transition-all duration-300 border border-transparent"
              >
                Je serai présent(e)
              </button>
              <button
                type="button"
                @click="rsvpForm.presence = false"
                :class="!rsvpForm.presence ? 'bg-red-600 text-white shadow-xl scale-105 shadow-red-600/20' : 'bg-neutral-50 text-neutral-400 hover:bg-neutral-100'"
                class="flex-1 px-8 py-5 rounded-2xl text-[11px] font-bold uppercase tracking-[0.2em] transition-all duration-300 border border-transparent"
              >
                Je serai absent(e)
              </button>
            </div>

            <!-- Form Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Prénom</label>
                <input v-model="rsvpForm.first_name" type="text" required class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300" />
              </div>
              <div class="space-y-1">
                <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Nom</label>
                <input v-model="rsvpForm.last_name" type="text" required class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300" />
              </div>
            </div>
            
            <div class="space-y-1">
              <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Email</label>
              <input v-model="rsvpForm.email" type="email" class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300" placeholder="Pour recevoir vos informations" />
            </div>

            <div v-if="rsvpForm.presence" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Accompagnants</label>
                <select v-model.number="rsvpForm.plus_ones" class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300 appearance-none">
                  <option v-for="n in 6" :key="n-1" :value="n-1">{{ n-1 === 0 ? 'Vient seul(e)' : n-1 + ' invité(s) supp.' }}</option>
                </select>
              </div>
              <div class="space-y-1">
                <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Restrictions alimentaires</label>
                <input v-model="rsvpForm.dietary_restrictions" type="text" placeholder="Allergies, régime..." class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300" />
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-[10px] uppercase tracking-widest text-neutral-400 font-bold ml-1">Petit mot pour nous</label>
              <textarea v-model="rsvpForm.message" rows="4" placeholder="Félicitations, questions..." class="w-full px-5 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300 resize-none"></textarea>
            </div>

            <button 
              type="submit" 
              :disabled="loading" 
              class="w-full py-5 rounded-2xl font-bold uppercase tracking-[0.3em] text-[12px] shadow-2xl transition-all duration-500 transform active:scale-[0.98] group relative overflow-hidden"
              :class="rsvpForm.presence ? 'bg-primary-900 text-white' : 'bg-neutral-800 text-white'"
            >
              <div class="absolute inset-0 bg-white/10 w-0 group-hover:w-full transition-all duration-500"></div>
              <span class="relative z-10">{{ loading ? 'Envoi en cours...' : 'Envoyer ma réponse' }}</span>
            </button>
          </form>
        </div>
      </div>

      <!-- Footer -->
      <footer class="py-12 bg-neutral-50 border-t border-neutral-100 flex flex-col items-center">
        <div class="w-8 h-[1px] bg-neutral-200 mb-6"></div>
        <p class="text-[10px] text-neutral-400 font-bold uppercase tracking-[0.4em] mb-2">Saas Wedding</p>
        <p class="text-[10px] text-neutral-300 uppercase tracking-widest">© 2026 — Votre histoire commence ici</p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
@keyframes music-bar {
  0%, 100% { height: 6px; }
  50% { height: 18px; }
}
.animate-music-bar-1 { animation: music-bar 0.6s ease-in-out infinite; }
.animate-music-bar-2 { animation: music-bar 0.6s ease-in-out 0.2s infinite; }
.animate-music-bar-3 { animation: music-bar 0.6s ease-in-out 0.4s infinite; }

@keyframes grow-width {
  from { width: 0; }
  to { width: 4rem; }
}
.animate-grow-width { animation: grow-width 1.5s ease-out infinite alternate; }

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fade-in { animation: fade-in 1.5s ease-out forwards; }

@keyframes scale-up {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-scale-up { animation: scale-up 0.5s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
</style>

<style scoped>
.bar-1 { animation: music 0.8s ease-in-out infinite; }
.bar-2 { animation: music 0.8s ease-in-out 0.2s infinite; }
.bar-3 { animation: music 0.8s ease-in-out 0.4s infinite; }

@keyframes music {
  0%, 100% { height: 8px; }
  50% { height: 20px; }
}
</style>
