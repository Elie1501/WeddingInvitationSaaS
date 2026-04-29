<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';

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

const handleRSVP = async () => {
  try {
    loading.value = true;
    error.value = '';
    await api.post('/guests/public/rsvp', {
      ...rsvpForm.value,
      event_id: cardData.value.event_id || cardData.value.id
    });
    successMessage.value = "Votre réponse a été enregistrée avec succès.";
    rsvpForm.value = { first_name: '', last_name: '', email: '', presence: true, plus_ones: 0, sub_guests: [], dietary_restrictions: '', message: '' };
  } catch (err) {
    error.value = "Erreur lors de l'enregistrement.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-[#FDFCFB] flex flex-col items-center selection:bg-[#C5A059] selection:text-white font-serif">
    
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

      <!-- RSVP -->
      <div v-if="cardData.has_rsvp_form" class="w-full max-w-2xl px-8 py-32 bg-white md:rounded-[3rem] md:mb-20 md:shadow-sm border-t border-gray-50">
        
        <div class="text-center mb-20 space-y-6">
          <span class="text-[10px] uppercase tracking-[0.5em] text-[#C5A059] font-black">Réponse attendue</span>
          <h3 class="text-5xl font-light italic text-[#1A1A1A]">Serez-vous des nôtres ?</h3>
        </div>

        <div v-if="successMessage" class="bg-[#F9F7F2] p-12 rounded-3xl text-center border border-[#C5A059]/20 animate-fade-in">
           <p class="text-xl italic text-[#1A1A1A]">{{ successMessage }}</p>
        </div>

        <form v-else @submit.prevent="handleRSVP" class="space-y-12">
          
          <div class="flex justify-center space-x-4">
            <button type="button" @click="rsvpForm.presence = true" 
              :class="rsvpForm.presence ? 'bg-[#1A1A1A] text-white shadow-xl' : 'bg-gray-50 text-gray-400'"
              class="flex-1 py-5 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all">
              Je serai présent(e)
            </button>
            <button type="button" @click="rsvpForm.presence = false" 
              :class="!rsvpForm.presence ? 'bg-[#1A1A1A] text-white shadow-xl' : 'bg-gray-50 text-gray-400'"
              class="flex-1 py-5 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all">
              Je serai absent(e)
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input v-model="rsvpForm.first_name" type="text" placeholder="Prénom" required class="w-full px-6 py-4 rounded-xl border border-gray-100 bg-gray-50/30 focus:bg-white focus:border-[#C5A059] outline-none transition-all" />
            <input v-model="rsvpForm.last_name" type="text" placeholder="Nom" required class="w-full px-6 py-4 rounded-xl border border-gray-100 bg-gray-50/30 focus:bg-white focus:border-[#C5A059] outline-none transition-all" />
          </div>

          <div v-if="rsvpForm.presence" class="space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <select v-model.number="rsvpForm.plus_ones" class="w-full px-6 py-4 rounded-xl border border-gray-100 bg-gray-50/30 focus:bg-white outline-none">
                <option v-for="n in 7" :key="n-1" :value="n-1">{{ n-1 === 0 ? 'Je viens seul(e)' : '+ ' + (n-1) + ' accompagnant(s)' }}</option>
              </select>
              <input v-model="rsvpForm.dietary_restrictions" type="text" placeholder="Allergies / Régime..." class="w-full px-6 py-4 rounded-xl border border-gray-100 bg-gray-50/30 focus:bg-white outline-none" />
            </div>

            <!-- Accompagnants -->
            <div v-if="rsvpForm.plus_ones > 0" class="space-y-6 animate-fade-in border-l-2 border-[#C5A059]/10 pl-6">
              <div v-for="(sub, index) in rsvpForm.sub_guests" :key="index" class="space-y-4">
                <p class="text-[10px] uppercase tracking-widest font-black text-[#C5A059]">Accompagnant {{ index + 1 }}</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input v-model="sub.first_name" type="text" placeholder="Prénom" required class="w-full px-6 py-3 rounded-xl border border-gray-100 bg-gray-50/20 focus:bg-white outline-none" />
                  <input v-model="sub.last_name" type="text" placeholder="Nom" required class="w-full px-6 py-3 rounded-xl border border-gray-100 bg-gray-50/20 focus:bg-white outline-none" />
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-[9px] uppercase tracking-widest text-gray-400 font-black ml-1">Message aux mariés</label>
            <textarea v-model="rsvpForm.message" rows="4" class="w-full px-6 py-4 rounded-xl border border-gray-100 bg-gray-50/30 focus:bg-white outline-none resize-none"></textarea>
          </div>

          <button type="submit" :disabled="loading" class="w-full py-6 bg-[#1A1A1A] text-white rounded-2xl text-[11px] font-black uppercase tracking-[0.4em] hover:bg-black transition-all shadow-xl disabled:opacity-50">
            {{ loading ? 'Envoi...' : 'Confirmer ma présence' }}
          </button>

        </form>
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
