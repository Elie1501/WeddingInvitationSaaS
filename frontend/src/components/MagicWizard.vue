<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const step = ref(1);
const totalSteps = 4;

const formData = ref({
  groomName: '',
  brideName: '',
  date: '',
  location: '',
  style: 'minimal'
});

const nextStep = () => {
  if (step.value < totalSteps) {
    step.value++;
  } else {
    finish();
  }
};

const prevStep = () => {
  if (step.value > 1) {
    step.value--;
  }
};

const finish = () => {
  // Sauvegarder les données temporairement pour la galerie
  localStorage.setItem('wizard_data', JSON.stringify(formData.value));
  router.push('/templates');
};

const progress = computed(() => (step.value / totalSteps) * 100);

const styles = [
  { id: 'minimal', name: 'Luxe Minimaliste', description: 'Épuré, moderne et intemporel', icon: '✨' },
  { id: 'classic', name: 'Classique Royal', description: 'Traditionnel, doré et majestueux', icon: '👑' },
  { id: 'bohemian', name: 'Bohème Chic', description: 'Naturel, floral et poétique', icon: '🌿' }
];

const selectStyle = (styleId) => {
  formData.value.style = styleId;
  nextStep();
};
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] flex flex-col items-center justify-center px-4 relative overflow-hidden font-serif">
    <!-- Éléments décoratifs -->
    <div class="absolute top-0 left-0 w-full h-1 bg-gray-200">
      <div class="h-full bg-[#C5A059] transition-all duration-700 ease-out" :style="{ width: progress + '%' }"></div>
    </div>
    
    <div class="max-w-2xl w-full text-center">
      
      <transition name="fade-slide" mode="out-in">
        <div :key="step" class="w-full">
        
          <div v-if="step === 1" class="space-y-12">
            <div class="space-y-4">
              <span class="text-[#C5A059] tracking-[0.3em] text-sm uppercase">L'Identité</span>
              <h2 class="text-5xl text-[#1A1A1A] leading-tight">Qui sont les deux étoiles de cette célébration ?</h2>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div class="space-y-2">
                <label class="block text-xs uppercase tracking-widest text-gray-400">Prénom 1</label>
                <input 
                  v-model="formData.groomName" 
                  type="text" 
                  placeholder="Ex: Alexandre"
                  class="w-full bg-transparent border-b-2 border-gray-200 py-4 text-2xl focus:border-[#C5A059] outline-none transition-colors text-center"
                />
              </div>
              <div class="space-y-2">
                <label class="block text-xs uppercase tracking-widest text-gray-400">Prénom 2</label>
                <input 
                  v-model="formData.brideName" 
                  type="text" 
                  placeholder="Ex: Éléonore"
                  class="w-full bg-transparent border-b-2 border-gray-200 py-4 text-2xl focus:border-[#C5A059] outline-none transition-colors text-center"
                />
              </div>
            </div>

            <button 
              @click="nextStep" 
              :disabled="!formData.groomName || !formData.brideName"
              class="mt-12 px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-lg hover:bg-black transition-all disabled:opacity-30 tracking-widest uppercase text-sm"
            >
              Continuer
            </button>
          </div>

          <div v-if="step === 2" class="space-y-12">
            <div class="space-y-4">
              <span class="text-[#C5A059] tracking-[0.3em] text-sm uppercase">Le Temps</span>
              <h2 class="text-5xl text-[#1A1A1A] leading-tight">À quel moment le monde s'arrêtera-t-il pour vous dire OUI ?</h2>
            </div>
            
            <div class="max-w-md mx-auto">
              <input 
                v-model="formData.date" 
                type="date" 
                class="w-full bg-transparent border-b-2 border-gray-200 py-4 text-3xl focus:border-[#C5A059] outline-none transition-colors text-center cursor-pointer"
              />
            </div>

            <div class="flex justify-center space-x-6">
              <button @click="prevStep" class="text-gray-400 hover:text-black transition-colors uppercase tracking-widest text-xs">Retour</button>
              <button 
                @click="nextStep" 
                :disabled="!formData.date"
                class="px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-lg hover:bg-black transition-all disabled:opacity-30 tracking-widest uppercase text-sm"
              >
                Suivant
              </button>
            </div>
          </div>

          <div v-if="step === 3" class="space-y-12">
            <div class="space-y-4">
              <span class="text-[#C5A059] tracking-[0.3em] text-sm uppercase">Le Lieu</span>
              <h2 class="text-5xl text-[#1A1A1A] leading-tight">Où allez-vous ancrer vos souvenirs ?</h2>
            </div>
            
            <div class="max-w-xl mx-auto">
              <input 
                v-model="formData.location" 
                type="text" 
                placeholder="Ex: Château de Versailles, France"
                class="w-full bg-transparent border-b-2 border-gray-200 py-4 text-2xl focus:border-[#C5A059] outline-none transition-colors text-center"
              />
            </div>

            <div class="flex justify-center space-x-6">
              <button @click="prevStep" class="text-gray-400 hover:text-black transition-colors uppercase tracking-widest text-xs">Retour</button>
              <button 
                @click="nextStep" 
                :disabled="!formData.location"
                class="px-12 py-4 bg-[#1A1A1A] text-white rounded-full text-lg hover:bg-black transition-all disabled:opacity-30 tracking-widest uppercase text-sm"
              >
                Suivant
              </button>
            </div>
          </div>

          <div v-if="step === 4" class="space-y-12">
            <div class="space-y-4">
              <span class="text-[#C5A059] tracking-[0.3em] text-sm uppercase">L'Ambiance</span>
              <h2 class="text-5xl text-[#1A1A1A] leading-tight">Quelle atmosphère souhaitez-vous respirer ?</h2>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                v-for="s in styles" 
                :key="s.id"
                @click="selectStyle(s.id)"
                class="group cursor-pointer p-8 bg-white border border-gray-100 rounded-2xl hover:border-[#C5A059] transition-all hover:shadow-2xl hover:shadow-[#C5A059]/10"
              >
                <div class="text-4xl mb-4 group-hover:scale-125 transition-transform duration-500">{{ s.icon }}</div>
                <h3 class="text-xl mb-2">{{ s.name }}</h3>
                <p class="text-sm text-gray-400 font-sans">{{ s.description }}</p>
              </div>
            </div>

            <div class="flex justify-center pt-8">
              <button @click="prevStep" class="text-gray-400 hover:text-black transition-colors uppercase tracking-widest text-xs">Retour</button>
            </div>
          </div>
          
        </div>
      </transition>

    </div>

    <!-- Citation de fond -->
    <div class="absolute bottom-12 text-gray-300 italic text-sm tracking-widest opacity-50">
      "Le design est l'ambassadeur silencieux de votre amour."
    </div>
  </div>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

input::placeholder {
  color: #E5E5E5;
}
</style>
