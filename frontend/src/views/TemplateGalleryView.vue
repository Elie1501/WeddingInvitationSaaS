<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const templates = ref([]);
const loading = ref(true);
const event = ref(null);
const eventId = route.query.eventId;

// Filters
const selectedPlan = ref('all');
const selectedStyle = ref('all');
const searchQuery = ref('');

const styles = [
  { id: 'all', label: 'Tout voir' },
  { id: 'modern', label: 'Moderne & Chic' },
  { id: 'classic', label: 'Classique & Élégance' },
  { id: 'boho', label: 'Bohème & Nature' },
  { id: 'luxury', label: 'Luxe & Prestige' }
];

const fetchTemplates = async () => {
  try {
    const response = await api.get('/templates/');
    templates.value = response.data;
  } catch (err) {
    console.error("Erreur templates", err);
  } finally {
    loading.value = false;
  }
};

const fetchEvent = async () => {
  try {
    let targetEventId = eventId;
    if (!targetEventId) {
      // Si pas d'ID dans l'URL, on récupère le dernier
      const res = await api.get('/events/mine/latest');
      targetEventId = res.data.event_id;
    }
    const response = await api.get(`/events/${targetEventId}`);
    event.value = response.data;
  } catch (err) {
    console.error("Erreur event", err);
  }
};

const filteredTemplates = computed(() => {
  return templates.value.filter(tpl => {
    const matchesPlan = selectedPlan.value === 'all' || tpl.required_plan === selectedPlan.value;
    const matchesSearch = tpl.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          tpl.description.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    // Logic for style filters
    let matchesStyle = selectedStyle.value === 'all';
    if (!matchesStyle) {
      const keywords = {
        'modern': ['modern', 'chic', 'minimal', 'épuré'],
        'classic': ['classic', 'elegance', 'traditionnel', 'intemporel'],
        'boho': ['bohemian', 'dream', 'nature', 'bohème', 'extérieur'],
        'romantic': ['romantic', 'floral', 'romantique', 'fleur', 'doux'],
        'luxury': ['royal', 'gold', 'luxe', 'prestige', 'glamour']
      };
      const currentKeywords = keywords[selectedStyle.value] || [];
      matchesStyle = currentKeywords.some(k => 
        tpl.name.toLowerCase().includes(k) || 
        tpl.description.toLowerCase().includes(k)
      );
    }

    return matchesPlan && matchesSearch && matchesStyle;
  });
});

const selectTemplate = async (template) => {
  if (template.required_plan === 'premium' && auth.user?.plan !== 'premium') {
    alert("Ce modèle est réservé aux membres Premium.");
    return;
  }

  try {
    loading.value = true;
    
    // On essaie de récupérer le cardId depuis l'objet event
    // Note : le backend renvoie souvent l'id de la carte dans event.card.id
    const cardId = event.value?.card?.id;
    
    console.log("Tentative de sélection pour Event:", eventId, "CardID:", cardId);

    if (!cardId) {
      alert("Désolé, nous ne trouvons pas l'invitation liée à cet événement. Essayez de recharger la page.");
      loading.value = false;
      return;
    }

    // On prépare la configuration initiale du template
    let manifest = {};
    try {
      manifest = JSON.parse(template.manifest_json);
    } catch (e) {
      manifest = template.manifest_json; // Déjà un objet
    }
    
    let configToSave = manifest.default_config || manifest;
    
    // S'assurer que les propriétés de thème existent pour le nouveau concepteur
    if (!configToSave.theme) {
      configToSave.theme = {
        primaryColor: configToSave.colors?.text || '#000000',
        secondaryColor: configToSave.colors?.background || '#ffffff',
        fontFamily: configToSave.fonts?.headings || 'serif'
      };
    }

    // Sauvegarde du choix de template
    await api.put(`/cards/${cardId}/save`, {
      template_id: template.id,
      config_json: JSON.stringify(configToSave)
    });
    
    console.log("Redirection vers l'éditeur...");
    router.push(`/cards/edit/${cardId}`);
  } catch (err) {
    console.error("Erreur sélection template :", err);
    alert("Une erreur est survenue lors de l'application du modèle. Vérifiez votre connexion.");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTemplates();
  fetchEvent();
});
</script>

<template>
  <div class="min-h-screen bg-white flex font-sans selection:bg-black selection:text-white">
    
    <!-- LEFT SIDEBAR FILTERS -->
    <aside class="w-80 border-r border-gray-100 p-12 flex flex-col fixed h-full bg-white z-20">
      <div class="mb-16">
        <span class="text-[10px] font-black uppercase tracking-[0.5em] text-gray-300 block mb-4">Studio Galerie</span>
        <h2 class="text-3xl font-black uppercase tracking-tighter">Filtres</h2>
      </div>

      <div class="space-y-12 flex-1">
        <!-- Search -->
        <div class="space-y-4">
          <label class="text-[9px] font-black uppercase tracking-widest text-gray-400">Rechercher</label>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Nom du modèle..." 
            class="w-full bg-gray-50 p-4 rounded-xl text-xs font-bold outline-none border border-transparent focus:border-black transition-all"
          >
        </div>

        <!-- Collection/Plans -->
        <div class="space-y-4">
          <label class="text-[9px] font-black uppercase tracking-widest text-gray-400">Collection</label>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="plan in [{id:'all', label:'Tout'}, {id:'classic', label:'Standard'}, {id:'premium', label:'Premium'}]"
              :key="plan.id"
              @click="selectedPlan = plan.id"
              :class="selectedPlan === plan.id ? 'bg-black text-white' : 'bg-gray-50 hover:bg-gray-100'"
              class="px-4 py-2 rounded-lg text-[10px] font-bold transition-all"
            >
              {{ plan.label }}
            </button>
          </div>
        </div>

        <!-- Styles -->
        <div class="space-y-4">
          <label class="text-[9px] font-black uppercase tracking-widest text-gray-400">Style</label>
          <div class="space-y-1">
            <button 
              v-for="style in styles"
              :key="style.id"
              @click="selectedStyle = style.id"
              :class="selectedStyle === style.id ? 'text-black translate-x-2' : 'text-gray-400 hover:text-black hover:translate-x-1'"
              class="w-full text-left py-2 text-xs font-bold transition-all flex items-center group"
            >
              <span class="w-2 h-2 rounded-full mr-3 transition-all" :class="selectedStyle === style.id ? 'bg-black scale-100' : 'bg-gray-200 scale-0 group-hover:scale-100'"></span>
              {{ style.label }}
            </button>
          </div>
        </div>

        <!-- Quick Info -->
        <div class="pt-12 border-t border-gray-100">
          <p class="text-[10px] text-gray-300 leading-relaxed font-medium italic">
            "Le design est l'ambassadeur silencieux de votre marque."
          </p>
        </div>
      </div>

      <div class="mt-auto pt-8 flex flex-col space-y-4">
        <button 
          @click="event?.card?.id ? router.push(`/cards/edit/${event.card.id}`) : router.push('/dashboard')" 
          class="text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-black transition-all flex items-center"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          Annuler / Retour
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 ml-80 p-12 md:p-24 bg-gray-50/30">
      
      <header class="mb-24 flex justify-between items-end">
        <div>
          <h1 class="text-7xl md:text-9xl font-black tracking-tighter uppercase leading-[0.8] text-black">
            L'Art du<br/><span class="text-gray-200 italic">Visuel.</span>
          </h1>
        </div>
        <div class="text-right">
          <span class="text-[60px] font-black tracking-tighter text-gray-100 leading-none">
            {{ filteredTemplates.length }}
          </span>
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-300">Modèles disponibles</p>
        </div>
      </header>

      <div v-if="loading" class="flex items-center justify-center py-40">
        <div class="w-12 h-12 border-t-2 border-black rounded-full animate-spin"></div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
        <div 
          v-for="tpl in filteredTemplates" 
          :key="tpl.id"
          @click="selectTemplate(tpl)"
          class="group cursor-pointer"
        >
          <div class="relative aspect-[3/4] overflow-hidden bg-white rounded-2xl shadow-sm group-hover:shadow-2xl transition-all duration-700 border border-gray-100">
            <img 
               :src="tpl.thumbnail_url" 
               class="absolute inset-0 w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110"
               alt="Template"
            />
            
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-8">
               <div class="translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                  <span class="text-[10px] font-black uppercase tracking-widest text-white/60 mb-2 block">
                    {{ tpl.required_plan === 'premium' ? 'Collection Privée' : 'Collection Libre' }}
                  </span>
                  <h3 class="text-2xl font-black text-white uppercase tracking-tighter mb-6">{{ tpl.name }}</h3>
                  <div class="flex items-center space-x-4">
                    <span class="px-6 py-3 bg-white text-black text-[10px] font-black uppercase tracking-widest rounded-full">Choisir</span>
                  </div>
               </div>
            </div>

            <!-- Premium Badge -->
            <div v-if="tpl.required_plan === 'premium'" class="absolute top-6 right-6 px-3 py-1 bg-amber-400 text-black text-[8px] font-black uppercase tracking-widest rounded-full">
               Premium
            </div>
          </div>
          
          <div class="mt-6 flex justify-between items-center px-2">
            <h4 class="text-[11px] font-black uppercase tracking-widest text-black">{{ tpl.name }}</h4>
            <span class="text-gray-300 font-serif italic">#{{ templates.indexOf(tpl) + 1 }}</span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredTemplates.length === 0" class="py-40 text-center">
        <p class="text-gray-300 text-xl font-medium">Aucun modèle ne correspond à vos critères.</p>
        <button @click="selectedPlan = 'all'; searchQuery = ''" class="mt-4 text-xs font-black uppercase tracking-widest border-b border-black">Réinitialiser</button>
      </div>

    </main>
  </div>
</template>
