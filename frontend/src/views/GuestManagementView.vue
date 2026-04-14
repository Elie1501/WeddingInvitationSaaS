<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { getPlanInfo } from '../service/plans';

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;
const auth = useAuthStore();

const guests = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const filterStatus = ref('all');


const planInfo = computed(() => getPlanInfo(auth.user?.plan || 'classic'));
const showAddGuest = ref(false);
const newGuest = ref({ 
  first_name: '', 
  last_name: '', 
  email: '', 
  rsvp_status: 'pending',
  plus_ones: 0,
  dietary_restrictions: '',
  message: ''
});
const importing = ref(false);
const fileInput = ref(null);

const fetchGuests = async () => {
  try {
    const response = await api.get(`/guests/event/${eventId}`);
    guests.value = response.data;
  } catch (err) {
    console.error("Erreur lors de la récupération des invités", err);
  } finally {
    loading.value = false;
  }
};

const addGuest = async () => {
  try {
    const res = await api.post('/guests/', { ...newGuest.value, event_id: parseInt(eventId) });
    guests.value.unshift(res.data);
    showAddGuest.value = false;
    newGuest.value = { 
      first_name: '', 
      last_name: '', 
      email: '', 
      rsvp_status: 'pending',
      plus_ones: 0,
      dietary_restrictions: '',
      message: ''
    };
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de l'ajout");
  }
};

const handleImportCSV = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  importing.value = true;
  try {
    const res = await api.post(`/guests/event/${eventId}/import/csv`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    alert(res.data.message);
    fetchGuests();
  } catch (err) {
    alert("Erreur lors de l'import : " + (err.response?.data?.detail || "Format invalide"));
  } finally {
    importing.value = false;
    event.target.value = null;
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const deleteGuest = async (id) => {
  if (!confirm("Supprimer cet invité ?")) return;
  try {
    await api.delete(`/guests/${id}`);
    guests.value = guests.value.filter(g => g.id !== id);
  } catch (err) {
    console.error("Erreur suppression", err);
  }
};

const filteredGuests = computed(() => {
  return guests.value.filter(g => {
    const matchesSearch = `${g.first_name} ${g.last_name}`.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesFilter = filterStatus.value === 'all' || g.rsvp_status === filterStatus.value;
    return matchesSearch && matchesFilter;
  });
});

const stats = computed(() => {
  return {
    total: guests.value.length,
    confirmed: guests.value.filter(g => g.rsvp_status === 'confirmed').length,
    pending: guests.value.filter(g => g.rsvp_status === 'pending').length,
    declined: guests.value.filter(g => g.rsvp_status === 'declined').length,
    totalPlusOnes: guests.value.filter(g => g.rsvp_status === 'confirmed').reduce((acc, g) => acc + (g.plus_ones || 0), 0)
  };
});

onMounted(fetchGuests);
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 font-sans">
    <nav class="bg-white border-b border-gray-200 h-16 flex items-center px-8 sticky top-0 z-10 justify-between">
      <div class="flex items-center">
        <button @click="router.push('/dashboard')" class="text-gray-400 hover:text-primary-600 mr-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <h1 class="text-lg font-semibold text-gray-900">Gestion des Invités</h1>
      </div>
      <div class="flex space-x-3">
        <input type="file" ref="fileInput" @change="handleImportCSV" accept=".csv" class="hidden">
        <button 
          @click="planInfo.can_export ? triggerFileInput() : alert('Import réservé au forfait Avancé')" 
          :class="!planInfo.can_export ? 'opacity-50 grayscale cursor-not-allowed' : ''"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 transition-colors"
        >
          {{ importing ? 'Import...' : 'Importer CSV' }}
          <svg v-if="!planInfo.can_export" class="w-3.5 h-3.5 ml-2 text-primary-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path></svg>
        </button>
        <button 
          @click="planInfo.can_export ? window.open(`http://localhost:8000/tables/event/${eventId}/export/csv`) : alert('Export réservé au forfait Avancé')" 
          :class="!planInfo.can_export ? 'opacity-50 grayscale cursor-not-allowed' : ''"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 transition-colors"
        >
          Exporter CSV
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 relative overflow-hidden">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Total Invités</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.total }} <span class="text-xs font-normal text-gray-400">/ {{ planInfo.max_guests }}</span></p>
          <div class="absolute bottom-0 left-0 w-full bg-gray-100 h-1">
            <div 
              class="h-1 transition-all duration-500" 
              :class="stats.total >= planInfo.max_guests ? 'bg-red-500' : 'bg-primary-500'"
              :style="{ width: `${Math.min((stats.total / planInfo.max_guests) * 100, 100)}%` }"
            ></div>
          </div>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <p class="text-xs font-bold text-green-500 uppercase tracking-widest mb-1">Confirmés</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.confirmed }}</p>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <p class="text-xs font-bold text-yellow-500 uppercase tracking-widest mb-1">En attente</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.pending }}</p>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <p class="text-xs font-bold text-red-500 uppercase tracking-widest mb-1">Déclinés</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.declined }}</p>
        </div>
      </div>

      <!-- Filters & Actions -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex-1 flex gap-4">
          <div class="relative flex-1 max-w-md">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </span>
            <input v-model="searchQuery" type="text" placeholder="Rechercher un invité..." class="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-xl text-sm focus:ring-primary-500 focus:border-primary-500 bg-gray-50">
          </div>
          <select v-model="filterStatus" class="bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-primary-500 focus:border-primary-500 px-4 py-2">
            <option value="all">Tous les statuts</option>
            <option value="confirmed">Confirmés</option>
            <option value="pending">En attente</option>
            <option value="declined">Déclinés</option>
          </select>
        </div>
        <button 
          @click="stats.total < planInfo.max_guests ? showAddGuest = true : alert('Limite atteinte')"
          :disabled="stats.total >= planInfo.max_guests"
          :class="stats.total >= planInfo.max_guests ? 'bg-gray-400' : 'bg-primary-600 hover:bg-primary-700'"
          class="text-white px-6 py-2 rounded-xl text-sm font-semibold transition-colors shadow-sm"
        >
          Ajouter un invité
        </button>
      </div>

      <!-- Guest Table -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div v-if="loading" class="p-20 flex justify-center">
           <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-primary-600"></div>
        </div>
        <div v-else-if="filteredGuests.length === 0" class="p-20 text-center text-gray-500">
           Aucun invité trouvé.
        </div>
        <table v-else class="min-w-full divide-y divide-gray-100">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Invité</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Statut</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Accomp.</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Restrictions / Message</th>
              <th class="px-6 py-3 text-right text-[10px] font-bold text-gray-400 uppercase tracking-widest">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="guest in filteredGuests" :key="guest.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold text-xs mr-3">
                    {{ guest.first_name[0] }}{{ guest.last_name[0] }}
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ guest.first_name }} {{ guest.last_name }}</div>
                    <div class="text-xs text-gray-400">{{ guest.email || 'Pas d\'email' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-700': guest.rsvp_status === 'confirmed',
                  'bg-yellow-100 text-yellow-700': guest.rsvp_status === 'pending',
                  'bg-red-100 text-red-700': guest.rsvp_status === 'declined'
                }" class="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider">
                  {{ guest.rsvp_status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ guest.plus_ones || 0 }}
              </td>
              <td class="px-6 py-4">
                <div class="max-w-xs">
                  <p v-if="guest.dietary_restrictions" class="text-xs text-red-400 mb-1 font-medium">🍴 {{ guest.dietary_restrictions }}</p>
                  <p v-if="guest.message" class="text-xs text-gray-500 italic">"{{ guest.message }}"</p>
                  <span v-if="!guest.dietary_restrictions && !guest.message" class="text-xs text-gray-300">-</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="deleteGuest(guest.id)" class="text-gray-400 hover:text-red-600 transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal Ajout Invité -->
    <div v-if="showAddGuest" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-lg w-full shadow-2xl overflow-y-auto max-h-[90vh]">
        <h2 class="text-2xl font-serif text-gray-900 mb-6">Ajouter un Invité</h2>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Prénom</label>
              <input v-model="newGuest.first_name" type="text" placeholder="Jean" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Nom</label>
              <input v-model="newGuest.last_name" type="text" placeholder="Dupont" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Email (facultatif)</label>
            <input v-model="newGuest.email" type="email" placeholder="jean.dupont@email.com" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Statut RSVP</label>
              <select v-model="newGuest.rsvp_status" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                <option value="pending">En attente</option>
                <option value="confirmed">Confirmé</option>
                <option value="declined">Décliné</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Accompagnants (+X)</label>
              <input v-model.number="newGuest.plus_ones" type="number" min="0" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Restrictions alimentaires</label>
            <input v-model="newGuest.dietary_restrictions" type="text" placeholder="Végétarien, Allergie aux noix..." class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Message</label>
            <textarea v-model="newGuest.message" rows="3" placeholder="Petit mot de l'invité..." class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all"></textarea>
          </div>
        </div>
        <div class="flex space-x-3 mt-8">
          <button @click="showAddGuest = false" class="flex-1 py-3 text-sm font-semibold text-gray-500 hover:bg-gray-50 rounded-xl transition-colors">Annuler</button>
          <button @click="addGuest" class="flex-1 py-3 text-sm font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-xl transition-colors shadow-lg shadow-primary-600/20">Ajouter</button>
        </div>
      </div>
    </div>
  </div>
</template>
