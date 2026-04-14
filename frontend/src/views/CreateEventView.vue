<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../service/api';

const router = useRouter();
const loading = ref(false);
const error = ref('');
const currentStep = ref(1);
const totalSteps = 4;

const eventData = ref({
  title: '',
  groom_name: '',
  bride_name: '',
  date: '',
  location: ''
});

const progressWidth = computed(() => {
  return (currentStep.value / totalSteps) * 100 + '%';
});

const nextStep = () => {
  if (currentStep.value < totalSteps) {
    currentStep.value++;
  } else {
    handleCreateEvent();
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const handleCreateEvent = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    // Vérification basique des champs critiques
    if (!eventData.value.groom_name || !eventData.value.bride_name || !eventData.value.title) {
      error.value = "Veuillez remplir les prénoms et le titre du projet.";
      loading.value = false;
      return;
    }

    const payload = {
      title: eventData.value.title,
      groom_name: eventData.value.groom_name,
      bride_name: eventData.value.bride_name,
      date: eventData.value.date || null,
      location: eventData.value.location || '',
      template_id: 'arche-royale', // Correction : Utiliser un ID qui existe vraiment
      has_cover_page: true,
      has_countdown: true
    };

    console.log("Envoi du payload :", payload);

    const response = await api.post('/events/', payload);

    const eventId = response.data.id;
    router.push({ path: '/templates', query: { eventId } });
  } catch (err) {
    console.error("Erreur complète :", err);
    if (err.response) {
      const detail = err.response.data?.detail;
      error.value = Array.isArray(detail) ? detail.map(d => d.msg).join(' | ') : (detail || `Erreur serveur (${err.response.status})`);
    } else {
      error.value = "Impossible de contacter le serveur. Vérifiez que le backend est lancé et accessible sur le port 8000.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-white text-black flex flex-col font-sans selection:bg-black selection:text-white">
    
    <!-- Progress Bar -->
    <div class="fixed top-0 left-0 w-full h-1 bg-gray-100 z-50">
      <div 
        class="h-full bg-black transition-all duration-1000 ease-out"
        :style="{ width: progressWidth }"
      ></div>
    </div>

    <!-- Header / Nav -->
    <header class="p-8 flex justify-between items-center relative z-10">
      <span class="text-[10px] font-black uppercase tracking-[0.5em] text-gray-400">Configuration Studio — v2.0</span>
      <button @click="router.push('/dashboard')" class="text-[10px] font-black uppercase tracking-widest hover:opacity-50 transition-all text-gray-500">Quitter</button>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex items-center justify-center p-8 relative overflow-hidden">
      
      <!-- Background Decorative Element -->
      <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.03]">
        <span class="text-[40vw] font-black uppercase tracking-tighter select-none">{{ currentStep }}</span>
      </div>

      <div class="max-w-3xl w-full relative z-10">
        
        <transition name="step-fade" mode="out-in">
          
          <!-- STEP 1: LES PRÉNOMS -->
          <div v-if="currentStep === 1" :key="1" class="space-y-12">
            <header>
              <span class="text-xs font-bold uppercase tracking-[0.3em] text-gray-300 mb-4 block">Étape 01</span>
              <h2 class="text-6xl md:text-8xl font-black uppercase tracking-tighter leading-none">
                Qui sont les <br/><span class="text-gray-100 italic">heureux élus ?</span>
              </h2>
            </header>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
              <div class="border-b-2 border-gray-100 focus-within:border-black transition-all py-4">
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Partenaire 01</label>
                <input v-model="eventData.groom_name" type="text" placeholder="Prénom" class="w-full bg-transparent text-3xl font-bold outline-none placeholder:text-gray-100">
              </div>
              <div class="border-b-2 border-gray-100 focus-within:border-black transition-all py-4">
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Partenaire 02</label>
                <input v-model="eventData.bride_name" type="text" placeholder="Prénom" class="w-full bg-transparent text-3xl font-bold outline-none placeholder:text-gray-100">
              </div>
            </div>
          </div>

          <!-- STEP 2: LE TITRE -->
          <div v-else-if="currentStep === 2" :key="2" class="space-y-12">
            <header>
              <span class="text-xs font-bold uppercase tracking-[0.3em] text-gray-300 mb-4 block">Étape 02</span>
              <h2 class="text-6xl md:text-8xl font-black uppercase tracking-tighter leading-none">
                Donnez un <br/><span class="text-gray-100 italic">nom au projet.</span>
              </h2>
            </header>
            <div class="border-b-2 border-gray-100 focus-within:border-black transition-all py-6">
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Titre de l'événement</label>
              <input v-model="eventData.title" type="text" placeholder="Ex: Notre Mariage" class="w-full bg-transparent text-4xl font-bold outline-none placeholder:text-gray-100">
            </div>
          </div>

          <!-- STEP 3: DATE & HEURE -->
          <div v-else-if="currentStep === 3" :key="3" class="space-y-12">
            <header>
              <span class="text-xs font-bold uppercase tracking-[0.3em] text-gray-300 mb-4 block">Étape 03</span>
              <h2 class="text-6xl md:text-8xl font-black uppercase tracking-tighter leading-none">
                Quand est-ce <br/><span class="text-gray-100 italic">prévu ?</span>
              </h2>
            </header>
            <div class="border-b-2 border-gray-100 focus-within:border-black transition-all py-6">
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Date & Heure de la cérémonie</label>
              <input v-model="eventData.date" type="datetime-local" class="w-full bg-transparent text-3xl font-bold outline-none [color-scheme:light]">
            </div>
          </div>

          <!-- STEP 4: LIEU -->
          <div v-else-if="currentStep === 4" :key="4" class="space-y-12">
            <header>
              <span class="text-xs font-bold uppercase tracking-[0.3em] text-gray-300 mb-4 block">Étape 04</span>
              <h2 class="text-6xl md:text-8xl font-black uppercase tracking-tighter leading-none">
                Où se déroule <br/><span class="text-gray-100 italic">la fête ?</span>
              </h2>
            </header>
            <div class="border-b-2 border-gray-100 focus-within:border-black transition-all py-6">
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Lieu ou adresse</label>
              <textarea v-model="eventData.location" placeholder="Ex: Château de Fontainebleau" rows="2" class="w-full bg-transparent text-3xl font-bold outline-none placeholder:text-gray-100 resize-none"></textarea>
            </div>
          </div>

        </transition>

        <!-- Error Message -->
        <div v-if="error" class="mt-8 text-red-500 text-[10px] font-black uppercase tracking-widest">{{ error }}</div>

      </div>
    </main>

    <!-- Footer Controls -->
    <footer class="p-8 flex justify-between items-center relative z-10">
      <button 
        v-if="currentStep > 1"
        @click="prevStep" 
        class="text-xs font-bold uppercase tracking-[0.2em] text-gray-400 hover:text-black transition-all flex items-center"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        Retour
      </button>
      <div v-else></div>

      <button 
        @click="nextStep"
        :disabled="loading"
        class="group flex items-center space-x-6 hover:space-x-12 transition-all duration-700"
      >
        <span class="text-2xl font-black uppercase tracking-tighter text-black">
          {{ loading ? 'Synchronisation...' : (currentStep === totalSteps ? 'Terminer & Design' : 'Suivant') }}
        </span>
        <div class="w-16 h-[2px] bg-black group-hover:w-32 transition-all duration-700"></div>
      </button>
    </footer>

  </div>
</template>

<style scoped>
.step-fade-enter-active, .step-fade-leave-active {
  transition: all 0.6s cubic-bezier(0.19, 1, 0.22, 1);
}
.step-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.step-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
