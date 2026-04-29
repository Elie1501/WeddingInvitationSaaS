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

const fetchData = async () => {
  try {
    const [tablesRes, guestsRes] = await Promise.all([
      api.get(`/tables/event/${eventId}`),
      api.get(`/guests/event/${eventId}`)
    ]);
    tables.value = tablesRes.data;
    // On garde tout le monde (confirmés ou en attente)
    guests.value = guestsRes.data.filter(g => g.rsvp_status === 'confirmed' || g.rsvp_status === 'pending');
  } catch (err) {
    console.error("Erreur chargement", err);
  } finally {
    loading.value = false;
  }
};

const createTable = async () => {
  try {
    const res = await api.post('/tables', { ...newTable.value, event_id: parseInt(eventId) });
    tables.value.push(res.data);
    showAddTable.value = false;
    newTable.value = { name: '', capacity: 10 };
  } catch (err) {
    alert("Erreur création table");
  }
};

const deleteTable = async (id) => {
  if (!confirm("Supprimer cette table ?")) return;
  try {
    await api.delete(`/tables/${id}`);
    tables.value = tables.value.filter(t => t.id !== id);
    fetchData();
  } catch (err) {
    console.error(err);
  }
};

const assignToTable = async (tableId, guestId) => {
  try {
    await api.post(`/tables/${tableId}/assign/${guestId}`);
    fetchData(); 
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur d'assignation");
  }
};

const unassignFromTable = async (tableId, guestId) => {
  try {
    await api.post(`/tables/${tableId}/unassign/${guestId}`);
    fetchData();
  } catch (err) {
    console.error(err);
  }
};

const onDragStart = (e, guestId) => {
  e.dataTransfer.setData('guestId', guestId);
};

const onDrop = async (e, tableId) => {
  const guestId = e.dataTransfer.getData('guestId');
  if (guestId) {
    await assignToTable(tableId, parseInt(guestId));
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
      <button @click="showAddTable = true" class="px-6 py-2 bg-primary-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-primary-600/20 hover:bg-primary-700 transition-all">
        + Ajouter une table
      </button>
    </nav>

    <div class="flex-1 flex overflow-hidden">
      <!-- Liste des personnes à placer -->
      <aside class="w-80 bg-white border-r border-gray-200 flex flex-col shadow-sm">
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
          <h2 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">À placer ({{ unassignedGuests.length }})</h2>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div 
            v-for="guest in unassignedGuests" 
            :key="guest.id"
            draggable="true"
            @dragstart="onDragStart($event, guest.id)"
            class="p-4 bg-white border border-gray-100 rounded-2xl shadow-sm cursor-move hover:border-primary-400 hover:shadow-md transition-all group"
          >
            <div class="flex items-center justify-between">
              <div class="flex flex-col">
                <span class="text-sm font-bold text-gray-800">{{ guest.first_name }} {{ guest.last_name }}</span>
                <span v-if="guest.parent_id" class="text-[9px] text-gray-400 uppercase font-black tracking-widest mt-1">Accompagnant</span>
              </div>
              <svg class="w-4 h-4 text-gray-300 group-hover:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path></svg>
            </div>
          </div>
          <div v-if="unassignedGuests.length === 0" class="text-center py-20 text-gray-300 text-xs italic">
            Tout le monde est assis !
          </div>
        </div>
      </aside>

      <!-- Zone des Tables -->
      <main class="flex-1 overflow-y-auto p-10 bg-gray-50 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-10">
        <div 
          v-for="table in tables" 
          :key="table.id"
          @dragover.prevent
          @drop="onDrop($event, table.id)"
          class="bg-white rounded-[3rem] border-2 border-dashed border-gray-200 p-8 flex flex-col h-fit min-h-[350px] transition-all hover:border-primary-300 group relative"
        >
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-serif text-gray-900">{{ table.name }}</h3>
              <p class="text-[10px] text-gray-400 uppercase font-black tracking-widest mt-1">
                {{ table.capacity - table.remaining_seats }} / {{ table.capacity }} PLACES
              </p>
            </div>
            <button @click="deleteTable(table.id)" class="text-gray-300 hover:text-red-500 transition-colors p-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
          </div>

          <!-- Jauge -->
          <div class="w-full bg-gray-100 rounded-full h-1.5 mb-8 overflow-hidden">
            <div 
              class="h-full rounded-full transition-all duration-700"
              :class="(table.capacity - table.remaining_seats) >= table.capacity ? 'bg-red-500' : 'bg-primary-500'"
              :style="{ width: `${((table.capacity - table.remaining_seats) / table.capacity) * 100}%` }"
            ></div>
          </div>

          <div class="flex-1 space-y-2">
            <div 
              v-for="guest in table.guests" 
              :key="guest.id"
              class="flex justify-between items-center p-3 rounded-2xl text-sm transition-all group/item"
              :class="guest.parent_id ? 'bg-gray-50 text-gray-600' : 'bg-primary-50 text-primary-900'"
            >
              <div class="flex items-center">
                <span class="font-bold">{{ guest.first_name }} {{ guest.last_name }}</span>
                <span v-if="guest.parent_id" class="ml-2 text-[8px] uppercase opacity-50 font-black">ACC.</span>
              </div>
              <button @click="unassignFromTable(table.id, guest.id)" class="opacity-0 group-hover/item:opacity-100 text-gray-400 hover:text-red-500 transition-all">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            
            <div v-if="table.guests.length === 0" class="flex flex-col items-center justify-center py-16 text-gray-300">
               <svg class="w-10 h-10 mb-2 opacity-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
               <span class="text-[9px] font-black uppercase tracking-[0.2em] opacity-40">Glisser ici</span>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal Table -->
    <div v-if="showAddTable" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-[2.5rem] p-10 max-w-sm w-full shadow-2xl">
        <h2 class="text-2xl font-serif text-gray-900 mb-8">Nouvelle Table</h2>
        <div class="space-y-6">
          <div>
            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Nom de la table</label>
            <input v-model="newTable.name" type="text" placeholder="Table d'honneur..." class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>
          <div>
            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Capacité</label>
            <input v-model="newTable.capacity" type="number" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
          </div>
        </div>
        <div class="flex space-x-3 mt-10">
          <button @click="showAddTable = false" class="flex-1 py-4 text-sm font-bold text-gray-400">Annuler</button>
          <button @click="createTable" class="flex-1 py-4 bg-primary-600 text-white rounded-2xl font-bold shadow-lg shadow-primary-600/30">Créer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cursor-move { cursor: grab; }
.cursor-move:active { cursor: grabbing; }
</style>
