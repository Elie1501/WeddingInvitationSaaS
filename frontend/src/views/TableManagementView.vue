<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;

const tables = ref([]);
const guests = ref([]);
const loading = ref(true);
const showAddTable = ref(false);
const newTable = ref({ name: '', capacity: 10 });
const newGuest = ref({ first_name: '', last_name: '' });
const addingGuest = ref(false);

const fetchData = async () => {
  try {
    const [tablesRes, guestsRes] = await Promise.all([
      api.get(`/tables/event/${eventId}`),
      api.get(`/guests/event/${eventId}`)
    ]);
    tables.value = tablesRes.data;
    // On garde les invités confirmés et en attente pour le plan de table
    guests.value = guestsRes.data.filter(g => g.rsvp_status === 'confirmed' || g.rsvp_status === 'pending');
  } catch (err) {
    console.error("Erreur lors du chargement des données", err);
  } finally {
    loading.value = false;
  }
};

const addGuestManually = async () => {
  if (!newGuest.value.first_name || !newGuest.value.last_name) return;
  try {
    addingGuest.value = true;
    const res = await api.post('/guests/', { 
      ...newGuest.value, 
      event_id: parseInt(eventId),
      rsvp_status: 'confirmed' 
    });
    guests.value.push(res.data);
    newGuest.value = { first_name: '', last_name: '' };
  } catch (err) {
    alert("Erreur lors de l'ajout de l'invité");
  } finally {
    addingGuest.value = false;
  }
};

const createTable = async () => {
  try {
    const res = await api.post('/tables/', { ...newTable.value, event_id: parseInt(eventId) });
    tables.value.push(res.data);
    showAddTable.value = false;
    newTable.value = { name: '', capacity: 10 };
  } catch (err) {
    alert("Erreur lors de la création de la table");
  }
};

const deleteTable = async (id) => {
  if (!confirm("Supprimer cette table ? Les invités seront désassignés.")) return;
  try {
    await api.delete(`/tables/${id}`);
    tables.value = tables.value.filter(t => t.id !== id);
  } catch (err) {
    console.error(err);
  }
};

const assignGuest = async (tableId, guestId) => {
  try {
    const res = await api.post(`/tables/${tableId}/assign/${guestId}`);
    const index = tables.value.findIndex(t => t.id === tableId);
    if (index !== -1) {
      tables.value[index] = res.data;
    }
    tables.value.forEach(t => {
      if (t.id !== tableId) {
        t.guests = t.guests.filter(g => g.id !== guestId);
      }
    });
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur d'assignation");
  }
};

const unassignGuest = async (tableId, guestId) => {
  try {
    const res = await api.post(`/tables/${tableId}/unassign/${guestId}`);
    const index = tables.value.findIndex(t => t.id === tableId);
    if (index !== -1) {
      tables.value[index] = res.data;
    }
  } catch (err) {
    console.error(err);
  }
};

const exportCSV = () => {
  window.open(`http://localhost:8000/tables/event/${eventId}/export/csv`, '_blank');
};

const handlePrint = () => {
  window.print();
};

const onDragStart = (e, guest) => {
  e.dataTransfer.setData('guestId', guest.id);
  e.dataTransfer.effectAllowed = 'move';
};

const onDrop = async (e, tableId) => {
  const guestId = e.dataTransfer.getData('guestId');
  if (guestId) {
    await assignGuest(tableId, parseInt(guestId));
  }
};

const unassignedGuests = computed(() => {
  const assignedIds = tables.value.flatMap(t => t.guests.map(g => g.id));
  return guests.value.filter(g => !assignedIds.includes(g.id));
});

onMounted(fetchData);
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">
    <nav class="bg-white border-b border-gray-200 h-16 flex items-center px-8 sticky top-0 z-10 justify-between">
      <div class="flex items-center">
        <button @click="router.push('/dashboard')" class="text-gray-400 hover:text-primary-600 mr-4 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <h1 class="text-lg font-semibold text-gray-900">Plan de Table</h1>
      </div>
      <div class="flex space-x-3">
        <button @click="handlePrint" class="hidden md:inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 transition-colors">
          Imprimer (PDF)
        </button>
        <button @click="exportCSV" class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 transition-colors">
          Exporter CSV
        </button>
        <button @click="showAddTable = true" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-xl shadow-sm text-white bg-primary-600 hover:bg-primary-700 transition-colors">
          + Ajouter une table
        </button>
      </div>
    </nav>

    <div class="flex-1 flex overflow-hidden">
      <!-- Sidebar : Invités à placer -->
      <aside class="w-80 bg-white border-r border-gray-200 flex flex-col shadow-sm">
        <div class="p-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-xs font-bold text-gray-400 uppercase tracking-widest">À placer ({{ unassignedGuests.length }})</h2>
        </div>
        
        <!-- Formulaire ajout rapide -->
        <div class="p-4 border-b border-gray-100 space-y-2">
          <div class="flex space-x-2">
            <input v-model="newGuest.first_name" type="text" placeholder="Prénom" class="flex-1 text-[10px] p-2 bg-gray-50 border border-gray-100 rounded-lg outline-none focus:ring-1 focus:ring-primary-400">
            <input v-model="newGuest.last_name" type="text" placeholder="Nom" class="flex-1 text-[10px] p-2 bg-gray-50 border border-gray-100 rounded-lg outline-none focus:ring-1 focus:ring-primary-400">
          </div>
          <button 
            @click="addGuestManually" 
            :disabled="addingGuest || !newGuest.first_name || !newGuest.last_name"
            class="w-full py-2 bg-primary-50 text-primary-600 text-[10px] font-bold uppercase tracking-widest rounded-lg hover:bg-primary-100 transition-colors disabled:opacity-50"
          >
            {{ addingGuest ? 'Ajout...' : '+ Ajouter à la main' }}
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-2">
          <div 
            v-for="guest in unassignedGuests" 
            :key="guest.id"
            draggable="true"
            @dragstart="onDragStart($event, guest)"
            class="p-3 bg-white border border-gray-100 rounded-xl shadow-sm cursor-move hover:border-primary-300 hover:shadow-md transition-all group"
          >
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700">{{ guest.first_name }} {{ guest.last_name }}</span>
              <svg class="w-4 h-4 text-gray-300 group-hover:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path></svg>
            </div>
          </div>
          <div v-if="unassignedGuests.length === 0" class="text-center py-10 text-gray-400 text-xs italic">
            Tous les invités sont placés !
          </div>
        </div>
      </aside>

      <!-- Zone Centrale : Les Tables -->
      <main class="flex-1 overflow-y-auto p-8 bg-gray-50 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="table in tables" 
          :key="table.id"
          @dragover.prevent
          @drop="onDrop($event, table.id)"
          class="bg-white rounded-3xl border-2 border-dashed border-gray-200 p-6 flex flex-col h-fit min-h-[300px] transition-all hover:border-primary-300 group relative"
        >
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-lg font-bold text-gray-900">{{ table.name }}</h3>
              <p class="text-xs text-gray-400 uppercase tracking-widest font-bold">
                {{ table.guests.length }} / {{ table.capacity }} places
              </p>
            </div>
            <button @click="deleteTable(table.id)" class="text-gray-300 hover:text-red-500 transition-colors p-1">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
          </div>

          <!-- Jauge de capacité -->
          <div class="w-full bg-gray-100 rounded-full h-1.5 mb-6">
            <div 
              class="h-1.5 rounded-full transition-all duration-500"
              :class="table.guests.length >= table.capacity ? 'bg-red-500' : 'bg-primary-500'"
              :style="{ width: `${(table.guests.length / table.capacity) * 100}%` }"
            ></div>
          </div>

          <div class="flex-1 space-y-2">
            <div 
              v-for="guest in table.guests" 
              :key="guest.id"
              class="flex justify-between items-center p-2.5 bg-primary-50 rounded-xl text-sm text-primary-900 group/item"
            >
              <span class="font-medium">{{ guest.first_name }} {{ guest.last_name }}</span>
              <button @click="unassignGuest(table.id, guest.id)" class="text-primary-300 hover:text-primary-600 opacity-0 group-hover/item:opacity-100 transition-all">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            
            <div v-if="table.guests.length === 0" class="flex flex-col items-center justify-center py-10 text-gray-300">
               <svg class="w-8 h-8 mb-2 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
               <span class="text-[10px] font-bold uppercase tracking-widest">Glissez un invité ici</span>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal Ajout Table -->
    <div v-if="showAddTable" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-sm w-full shadow-2xl">
        <h2 class="text-2xl font-serif text-gray-900 mb-6">Nouvelle Table</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Nom de la table</label>
            <input v-model="newTable.name" type="text" placeholder="Table d'honneur, Table 1..." class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Capacité (personnes)</label>
            <input v-model="newTable.capacity" type="number" class="w-full px-4 py-3 rounded-xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>
        </div>
        <div class="flex space-x-3 mt-8">
          <button @click="showAddTable = false" class="flex-1 py-3 text-sm font-semibold text-gray-500 hover:bg-gray-50 rounded-xl transition-colors">Annuler</button>
          <button @click="createTable" class="flex-1 py-3 text-sm font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-xl transition-colors shadow-lg shadow-primary-600/20">Créer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cursor-move { cursor: grab; }
.cursor-move:active { cursor: grabbing; }
</style>
