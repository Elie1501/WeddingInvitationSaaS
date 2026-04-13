<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { getPlanInfo } from '../service/plans';

const events = ref([]);
const loading = ref(true);
const auth = useAuthStore();
const router = useRouter();

const planInfo = computed(() => getPlanInfo(auth.user?.plan || 'classic'));
const showApiModal = ref(false);
const showPlanModal = ref(false);
const planUpdateLoading = ref(false);

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};

const handleUpdatePlan = async (newPlan) => {
  try {
    planUpdateLoading.value = true;
    await auth.updatePlan(newPlan);
    showPlanModal.value = false;
  } catch (err) {
    alert("Une erreur est survenue lors du changement de forfait.");
  } finally {
    planUpdateLoading.value = false;
  }
};

const goToTables = (eventId) => {
  if (!planInfo.value.can_use_tables) {
    alert(`Le plan de table est réservé aux forfaits Avancé. (Votre forfait actuel : ${planInfo.value.name})`);
    return;
  }
  router.push(`/events/${eventId}/tables`);
};

const handleDeleteEvent = async (eventId) => {
  if (!confirm("Êtes-vous sûr de vouloir supprimer cet événement ? Cette action est irréversible et supprimera également l'invitation associée.")) {
    return;
  }
  
  try {
    await api.delete(`/events/${eventId}`);
    events.value = events.value.filter(e => e.id !== eventId);
  } catch (err) {
    alert("Erreur lors de la suppression de l'événement.");
  }
};

onMounted(async () => {
  if (!auth.user) {
    await auth.fetchMe();
  }
  try {
    const response = await api.get('/events/');
    events.value = response.data;
  } catch (err) {
    console.error("Erreur lors de la récupération des événements", err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 pb-20">
    <!-- Navbar/Header élégant -->
    <nav class="bg-white border-b border-primary-100 sticky top-0 z-50 shadow-sm shadow-primary-900/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20">
          <div class="flex items-center">
            <h1 class="text-2xl text-primary-800">Saas Wedding</h1>
          </div>
          <div class="flex items-center space-x-6">
             <div v-if="auth.user" class="flex flex-col items-end">
                <span class="text-gray-900 font-sans text-sm font-medium">{{ auth.user.email }}</span>
                <div class="flex items-center">
                  <span :class="{
                    'text-gray-500': auth.user.plan === 'classic',
                    'text-primary-600': auth.user.plan === 'premium'
                  }" class="text-[10px] font-bold uppercase tracking-widest mr-2">{{ planInfo.name }}</span>
                  <button @click="showPlanModal = true" class="text-[10px] text-primary-500 hover:underline">Modifier</button>
                </div>
             </div>
             <button @click="handleLogout" class="text-gray-500 hover:text-red-500 transition-colors font-sans text-sm font-medium">Déconnexion</button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-12">
        <div>
          <h2 class="text-4xl text-gray-900 mb-2">Mes Événements</h2>
          <p class="text-gray-500 font-sans">Gérez vos invitations, listes d'invités et plans de table avec élégance.</p>
          <div v-if="events.length >= planInfo.max_sites" class="mt-4">
             <span class="text-xs font-bold text-amber-600 bg-amber-50 px-3 py-1.5 rounded-full border border-amber-100 transition-all">
               Limite de sites atteinte pour le forfait {{ planInfo.name }} ({{ planInfo.max_sites }})
             </span>
          </div>
        </div>
        <button 
          @click="events.length < planInfo.max_sites ? $router.push('/events/create') : alert('Limite de sites atteinte.')" 
          :class="events.length >= planInfo.max_sites ? 'opacity-50 grayscale cursor-not-allowed' : 'bg-primary-600 hover:bg-primary-700'"
          class="mt-6 md:mt-0 inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-full text-white shadow-md shadow-primary-600/20 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 font-sans"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
          Créer un événement
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-20">
         <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>

      <!-- Grid d'événements -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="event in events" :key="event.id" class="bg-white rounded-2xl p-8 shadow-sm shadow-primary-900/5 border border-primary-100 hover:shadow-lg hover:shadow-primary-900/10 transition-all duration-300 group flex flex-col h-full">
          
          <div class="flex-grow">
            <div class="flex justify-between items-start mb-6">
              <span 
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium font-sans tracking-wide"
                :class="event.card?.is_published ? 'bg-secondary-100 text-secondary-800' : 'bg-gray-100 text-gray-600'"
              >
                {{ event.card?.is_published ? 'En ligne' : 'Brouillon' }}
              </span>
            </div>
            
            <h3 class="text-2xl text-gray-900 mb-4 group-hover:text-primary-700 transition-colors">{{ event.title }}</h3>
            
            <div class="space-y-3 font-sans text-gray-600 text-sm">
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {{ new Date(event.date).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                {{ event.location }}
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-gray-100 flex flex-col space-y-3 font-sans">
             <button 
               @click="event.card ? $router.push(`/cards/edit/${event.card.id}`) : null"
               class="w-full py-2.5 px-4 bg-primary-50 hover:bg-primary-100 text-primary-800 rounded-lg text-sm font-medium transition-colors border border-primary-200"
             >
               Éditer l'invitation
             </button>
             <button @click="$router.push(`/events/${event.id}/guests`)" class="w-full py-2.5 px-4 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200 shadow-sm">
               Gérer les invités (RSVP)
             </button>
             <button 
                @click="goToTables(event.id)" 
                :class="!planInfo.can_use_tables ? 'opacity-50 grayscale cursor-not-allowed' : ''"
                class="w-full py-2.5 px-4 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200 shadow-sm flex items-center justify-center"
             >
               Plan de table
               <svg v-if="!planInfo.can_use_tables" class="w-3.5 h-3.5 ml-2 text-primary-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path></svg>
             </button>
             <button 
                @click="handleDeleteEvent(event.id)"
                class="w-full py-2.5 px-4 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg text-sm font-medium transition-colors border border-red-100 flex items-center justify-center"
             >
               Supprimer l'événement
             </button>
             <a v-if="event.card?.is_published" :href="'/cards/' + event.card.slug" target="_blank" class="text-center text-xs text-primary-600 hover:text-primary-800 underline mt-2">
               Voir la carte publique
             </a>
          </div>

        </div>
      </div>

    </main>

    <!-- Modal API (Developer only) -->
    <div v-if="showApiModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-2xl w-full shadow-2xl">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-2xl font-serif text-gray-900">Documentation API</h2>
          <button @click="showApiModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <div class="space-y-6">
          <div class="bg-gray-50 p-4 rounded-2xl border border-gray-100">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Votre Token d'API (JWT)</p>
            <div class="bg-white p-3 rounded-xl border border-gray-200 font-mono text-[10px] break-all text-gray-600">
              {{ auth.token }}
            </div>
          </div>
          <div class="space-y-3">
             <p class="text-sm text-gray-600">Utilisez ce token dans le header <code class="bg-gray-100 px-1 rounded">Authorization: Bearer [TOKEN]</code> pour vos requêtes automatisées.</p>
             <div class="bg-gray-900 text-gray-300 p-4 rounded-xl font-mono text-xs">
               curl -X GET "http://localhost:8000/events/" \<br>
               &nbsp;&nbsp;&nbsp;&nbsp;-H "Authorization: Bearer your_token"
             </div>
          </div>
        </div>
        <button @click="showApiModal = false" class="w-full mt-8 py-3 bg-secondary-600 text-white rounded-xl font-semibold hover:bg-secondary-700 transition-colors">Fermer</button>
      </div>
    </div>
    <!-- Modal Forfait -->
    <div v-if="showPlanModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-xl w-full shadow-2xl">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-2xl text-gray-900">Gérer mon forfait</h2>
          <button @click="showPlanModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Classic -->
            <div 
              class="border-2 rounded-2xl p-6 transition-all"
              :class="auth.user.plan === 'classic' ? 'border-primary-600 bg-primary-50' : 'border-gray-100 hover:border-primary-200'"
            >
              <div class="flex justify-between items-start mb-4">
                <div class="flex flex-col">
                  <h3 class="font-bold text-lg text-gray-900">Classic</h3>
                  <span class="text-primary-600 font-bold text-sm">45 €</span>
                </div>
                <span v-if="auth.user.plan === 'classic'" class="bg-primary-600 text-white text-[10px] px-2 py-0.5 rounded-full uppercase tracking-widest">Actuel</span>
              </div>
              <ul class="text-sm text-gray-600 space-y-2 mb-6 font-sans">
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Jusqu'à 100 invités</li>
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Plan de table complet</li>
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> 1 site d'invitation</li>
              </ul>
              <button 
                v-if="auth.user.plan !== 'classic'"
                @click="handleUpdatePlan('classic')"
                :disabled="planUpdateLoading"
                class="w-full py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg text-sm font-medium transition-colors"
              >
                Choisir Classic
              </button>
            </div>

            <!-- Premium -->
            <div 
              class="border-2 rounded-2xl p-6 transition-all"
              :class="auth.user.plan === 'premium' ? 'border-primary-600 bg-primary-50' : 'border-gray-100 hover:border-primary-200'"
            >
              <div class="flex justify-between items-start mb-4">
                <h3 class="font-bold text-lg text-gray-900">Premium</h3>
                <span v-if="auth.user.plan === 'premium'" class="bg-primary-600 text-white text-[10px] px-2 py-0.5 rounded-full uppercase tracking-widest">Actuel</span>
              </div>
              <ul class="text-sm text-gray-600 space-y-2 mb-6 font-sans">
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Jusqu'à 500 invités</li>
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> 5 sites d'invitation</li>
                <li class="flex items-center"><svg class="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Formulaire RSVP</li>
              </ul>
              <button 
                v-if="auth.user.plan !== 'premium'"
                @click="handleUpdatePlan('premium')"
                :disabled="planUpdateLoading"
                class="w-full py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors shadow-md shadow-primary-600/20"
              >
                Passer en Premium
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
