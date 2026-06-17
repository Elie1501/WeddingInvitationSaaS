<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import UpgradeModal from '../components/UpgradeModal.vue';

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;
const authStore = useAuthStore();
const isPremium = computed(() => authStore.user?.plan === 'premium');

// ── État principal ────────────────────────────────────────────────────────────
const tables = ref([]);
const guests = ref([]);
const loading = ref(true);

// ── Modals ────────────────────────────────────────────────────────────────────
const showAddTable    = ref(false);
const newTable        = ref({ name: '', capacity: 10 });

const showAddGuest    = ref(false);
const newGuest        = ref({ first_name: '', last_name: '' });
const savingGuest     = ref(false);

const showEditGuest   = ref(false);
const editingGuest    = ref(null);
const editGuestData   = ref({ first_name: '', last_name: '' });
const savingEdit      = ref(false);

const showUpgradeModal = ref(false);
const exportingCsv    = ref(false);

// ── Chargement ────────────────────────────────────────────────────────────────
const fetchData = async () => {
  try {
    const [tablesRes, guestsRes] = await Promise.all([
      api.get(`/tables/event/${eventId}`),
      api.get(`/guests/event/${eventId}`)
    ]);
    tables.value = tablesRes.data;
    guests.value = guestsRes.data.filter(g => g.rsvp_status !== 'declined');
  } catch (err) {
    console.error("Erreur chargement", err);
  } finally {
    loading.value = false;
  }
};

// ── Tables ────────────────────────────────────────────────────────────────────
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

// ── Invités — ajout depuis le plan de table ───────────────────────────────────
const addGuest = async () => {
  if (!newGuest.value.first_name.trim() || !newGuest.value.last_name.trim()) return;
  savingGuest.value = true;
  try {
    await api.post('/guests', {
      first_name: newGuest.value.first_name.trim(),
      last_name:  newGuest.value.last_name.trim(),
      event_id:   parseInt(eventId),
      rsvp_status: 'confirmed',
    });
    showAddGuest.value = false;
    newGuest.value = { first_name: '', last_name: '' };
    await fetchData();
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de l'ajout");
  } finally {
    savingGuest.value = false;
  }
};

// ── Invités — édition ─────────────────────────────────────────────────────────
const openEditGuest = (guest) => {
  editingGuest.value = guest;
  editGuestData.value = { first_name: guest.first_name, last_name: guest.last_name };
  showEditGuest.value = true;
};

const saveEditGuest = async () => {
  if (!editGuestData.value.first_name.trim() || !editGuestData.value.last_name.trim()) return;
  savingEdit.value = true;
  try {
    await api.patch(`/guests/${editingGuest.value.id}`, {
      first_name: editGuestData.value.first_name.trim(),
      last_name:  editGuestData.value.last_name.trim(),
    });
    showEditGuest.value = false;
    editingGuest.value = null;
    await fetchData();
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de la modification");
  } finally {
    savingEdit.value = false;
  }
};

// ── Assignation drag & drop ───────────────────────────────────────────────────
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

const onDragStart = (e, guestId) => { e.dataTransfer.setData('guestId', guestId); };
const onDrop = async (e, tableId) => {
  const guestId = e.dataTransfer.getData('guestId');
  if (guestId) await assignToTable(tableId, parseInt(guestId));
};

// Mobile : assignation via menu déroulant (le drag & drop HTML5 ne fonctionne pas au toucher)
const onMobileAssign = async (e, guestId) => {
  const tableId = parseInt(e.target.value);
  if (tableId) await assignToTable(tableId, guestId);
  e.target.value = '';
};

// ── Export CSV ────────────────────────────────────────────────────────────────
const exportCsv = async () => {
  if (!isPremium.value) { showUpgradeModal.value = true; return; }
  exportingCsv.value = true;
  try {
    const res = await api.get(`/tables/event/${eventId}/export/csv`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement('a');
    a.href = url;
    a.download = `plan_de_table.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (err) {
    if (err.response?.status === 403 && !isPremium.value) showUpgradeModal.value = true;
    else if (err.response?.status === 403) alert("Accès refusé.");
    else alert("Erreur lors de l'export CSV");
  } finally {
    exportingCsv.value = false;
  }
};

// ── Computed ──────────────────────────────────────────────────────────────────
const unassignedGuests = computed(() => {
  const assignedIds = tables.value.flatMap(t => t.guests.map(g => g.id));
  return guests.value.filter(g => !assignedIds.includes(g.id));
});

onMounted(fetchData);
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">

    <!-- ── NAVBAR ── -->
    <nav class="bg-white border-b border-gray-200 min-h-16 py-2 flex items-center px-4 sm:px-8 sticky top-0 z-10 justify-between gap-2">
      <div class="flex items-center gap-2 sm:gap-4 min-w-0">
        <button @click="router.push('/dashboard')" class="text-gray-400 hover:text-primary-600 transition-colors shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        </button>
        <h1 class="text-base sm:text-lg font-semibold text-gray-900 truncate">Plan de Table</h1>
      </div>

      <div class="flex items-center gap-2 sm:gap-3 shrink-0">
        <!-- Export CSV — Premium only -->
        <button
          @click="exportCsv"
          :disabled="exportingCsv"
          class="flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-sm font-semibold transition-all"
          :class="isPremium
            ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'
            : 'bg-gray-50 text-gray-400 border border-gray-200 hover:bg-amber-50 hover:text-amber-600 hover:border-amber-200'"
          :title="isPremium ? 'Exporter le plan de table en CSV' : 'Export CSV — Forfait Premium requis'"
        >
          <svg v-if="isPremium && !exportingCsv" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          <svg v-else-if="!isPremium" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M18 8h-1V6A5 5 0 007 6v2H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10a2 2 0 00-2-2zm-6 9a2 2 0 110-4 2 2 0 010 4zm3.1-9H8.9V6a3.1 3.1 0 016.2 0v2z"/>
          </svg>
          <span v-if="exportingCsv" class="w-3.5 h-3.5 border-2 border-emerald-300 border-t-emerald-600 rounded-full animate-spin"></span>
          <span class="hidden sm:inline">Export CSV</span>
          <span class="sm:hidden">CSV</span>
        </button>

        <button @click="showAddTable = true" class="px-3 sm:px-6 py-2 bg-primary-600 text-white text-sm font-bold rounded-xl shadow-lg shadow-primary-600/20 hover:bg-primary-700 transition-all whitespace-nowrap">
          + <span class="hidden sm:inline">Ajouter une </span>Table
        </button>
      </div>
    </nav>

    <!-- ── CORPS ── -->
    <div class="flex-1 flex flex-col lg:flex-row overflow-hidden">

      <!-- ─ Sidebar : invités à placer (en haut sur mobile) ─ -->
      <aside class="w-full lg:w-80 max-h-[38vh] lg:max-h-none bg-white border-b lg:border-b-0 lg:border-r border-gray-200 flex flex-col shadow-sm shrink-0">
        <div class="p-5 border-b border-gray-100 bg-gray-50/50 flex items-center justify-between">
          <h2 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">
            À placer ({{ unassignedGuests.length }})
          </h2>
          <button
            @click="showAddGuest = true"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-wider text-primary-600 bg-primary-50 hover:bg-primary-100 transition-colors"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
            Personne
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-2">
          <div
            v-for="guest in unassignedGuests"
            :key="guest.id"
            draggable="true"
            @dragstart="onDragStart($event, guest.id)"
            class="p-3.5 bg-white border border-gray-100 rounded-2xl shadow-sm cursor-move hover:border-primary-400 hover:shadow-md transition-all group flex items-center justify-between"
          >
            <div class="flex flex-col min-w-0">
              <span class="text-sm font-bold text-gray-800 truncate">{{ guest.first_name }} {{ guest.last_name }}</span>
              <span v-if="guest.parent_id" class="text-[9px] text-gray-400 uppercase font-black tracking-widest mt-0.5">Accompagnant</span>
            </div>
            <div class="flex items-center gap-1 shrink-0 ml-2">
              <!-- Mobile : menu d'assignation tactile -->
              <select
                v-if="tables.length"
                @click.stop
                @change="onMobileAssign($event, guest.id)"
                class="lg:hidden text-[11px] border border-gray-200 rounded-lg px-1.5 py-1 bg-gray-50 text-gray-600 max-w-[92px]"
                title="Placer à une table"
              >
                <option value="">Placer à…</option>
                <option v-for="t in tables" :key="t.id" :value="t.id">{{ t.name }}</option>
              </select>
              <!-- Icône crayon (toujours visible sur mobile) -->
              <button
                @click.stop="openEditGuest(guest)"
                class="p-1.5 rounded-lg opacity-100 lg:opacity-0 lg:group-hover:opacity-100 text-gray-400 hover:text-primary-600 hover:bg-primary-50 transition-all"
                title="Modifier"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                </svg>
              </button>
              <!-- Poignée drag (desktop) -->
              <svg class="hidden lg:block w-4 h-4 text-gray-300 group-hover:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/></svg>
            </div>
          </div>

          <div v-if="unassignedGuests.length === 0 && !loading" class="text-center py-16 text-gray-300 text-xs italic space-y-1">
            <div>Tout le monde est assis !</div>
          </div>
        </div>
      </aside>

      <!-- ─ Zone tables ─ -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-10 bg-gray-50 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 sm:gap-10 content-start">
        <div
          v-for="table in tables"
          :key="table.id"
          @dragover.prevent
          @drop="onDrop($event, table.id)"
          class="bg-white rounded-3xl sm:rounded-[3rem] border-2 border-dashed border-gray-200 p-5 sm:p-8 flex flex-col h-fit min-h-[280px] sm:min-h-[350px] transition-all hover:border-primary-300 group relative"
        >
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-serif text-gray-900">{{ table.name }}</h3>
              <p class="text-[10px] text-gray-400 uppercase font-black tracking-widest mt-1">
                {{ table.capacity - table.remaining_seats }} / {{ table.capacity }} PLACES
              </p>
            </div>
            <button @click="deleteTable(table.id)" class="text-gray-300 hover:text-red-500 transition-colors p-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>

          <!-- Jauge de remplissage -->
          <div class="w-full bg-gray-100 rounded-full h-1.5 mb-8 overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-700"
              :class="(table.capacity - table.remaining_seats) >= table.capacity ? 'bg-red-500' : 'bg-primary-500'"
              :style="{ width: `${((table.capacity - table.remaining_seats) / table.capacity) * 100}%` }"
            ></div>
          </div>

          <!-- Liste invités assis -->
          <div class="flex-1 space-y-2">
            <div
              v-for="guest in table.guests"
              :key="guest.id"
              class="flex justify-between items-center p-3 rounded-2xl text-sm transition-all group/item"
              :class="guest.parent_id ? 'bg-gray-50 text-gray-600' : 'bg-primary-50 text-primary-900'"
            >
              <div class="flex items-center gap-2 min-w-0">
                <span class="font-bold truncate">{{ guest.first_name }} {{ guest.last_name }}</span>
                <span v-if="guest.parent_id" class="text-[8px] uppercase opacity-50 font-black shrink-0">ACC.</span>
              </div>
              <div class="flex items-center gap-1 opacity-100 lg:opacity-0 lg:group-hover/item:opacity-100 transition-all shrink-0">
                <!-- Crayon -->
                <button @click="openEditGuest(guest)" class="p-1 rounded-lg text-gray-400 hover:text-primary-600 hover:bg-primary-100 transition-colors" title="Modifier">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                  </svg>
                </button>
                <!-- Retirer -->
                <button @click="unassignFromTable(table.id, guest.id)" class="p-1 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors" title="Retirer de la table">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>

            <div v-if="table.guests.length === 0" class="flex flex-col items-center justify-center py-16 text-gray-300">
              <svg class="w-10 h-10 mb-2 opacity-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
              <span class="text-[9px] font-black uppercase tracking-[0.2em] opacity-40">Glisser ici</span>
            </div>
          </div>
        </div>

        <!-- Placeholder si aucune table -->
        <div v-if="!loading && tables.length === 0" class="col-span-full flex flex-col items-center justify-center py-32 text-gray-300 space-y-3">
          <svg class="w-16 h-16 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M3 6h18M3 14h18M3 18h18"/></svg>
          <p class="text-sm font-black uppercase tracking-widest opacity-40">Aucune table — commencez par en créer une</p>
        </div>
      </main>
    </div>

    <!-- ════ MODAL : Nouvelle table ════ -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showAddTable" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showAddTable = false">
          <div class="bg-white rounded-[2.5rem] p-10 max-w-sm w-full shadow-2xl">
            <h2 class="text-2xl font-serif text-gray-900 mb-8">Nouvelle Table</h2>
            <div class="space-y-6">
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Nom de la table</label>
                <input v-model="newTable.name" type="text" placeholder="Table d'honneur..." @keyup.enter="createTable"
                       class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
              </div>
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Capacité</label>
                <input v-model.number="newTable.capacity" type="number" min="1"
                       class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
              </div>
            </div>
            <div class="flex space-x-3 mt-10">
              <button @click="showAddTable = false" class="flex-1 py-4 text-sm font-bold text-gray-400 hover:text-gray-600 transition-colors">Annuler</button>
              <button @click="createTable" class="flex-1 py-4 bg-primary-600 text-white rounded-2xl font-bold shadow-lg shadow-primary-600/30 hover:bg-primary-700 transition-all">Créer</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ════ MODAL : Ajouter une personne ════ -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showAddGuest" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showAddGuest = false">
          <div class="bg-white rounded-[2.5rem] p-10 max-w-sm w-full shadow-2xl">
            <h2 class="text-2xl font-serif text-gray-900 mb-2">Ajouter une personne</h2>
            <p class="text-xs text-gray-400 mb-8">La personne sera ajoutée à la liste des invités (statut : confirmé).</p>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Prénom</label>
                  <input v-model="newGuest.first_name" type="text" autofocus @keyup.enter="addGuest"
                         class="w-full px-4 py-3.5 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Nom</label>
                  <input v-model="newGuest.last_name" type="text" @keyup.enter="addGuest"
                         class="w-full px-4 py-3.5 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                </div>
              </div>
            </div>
            <div class="flex space-x-3 mt-8">
              <button @click="showAddGuest = false" class="flex-1 py-4 text-sm font-bold text-gray-400 hover:text-gray-600 transition-colors">Annuler</button>
              <button @click="addGuest" :disabled="savingGuest || !newGuest.first_name.trim() || !newGuest.last_name.trim()"
                      class="flex-1 py-4 bg-primary-600 text-white rounded-2xl font-bold shadow-lg shadow-primary-600/30 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
                {{ savingGuest ? 'Ajout...' : 'Ajouter' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ════ MODAL : Modifier une personne ════ -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showEditGuest" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showEditGuest = false">
          <div class="bg-white rounded-[2.5rem] p-10 max-w-sm w-full shadow-2xl">
            <h2 class="text-2xl font-serif text-gray-900 mb-8">Modifier la personne</h2>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Prénom</label>
                  <input v-model="editGuestData.first_name" type="text" autofocus @keyup.enter="saveEditGuest"
                         class="w-full px-4 py-3.5 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Nom</label>
                  <input v-model="editGuestData.last_name" type="text" @keyup.enter="saveEditGuest"
                         class="w-full px-4 py-3.5 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                </div>
              </div>
            </div>
            <div class="flex space-x-3 mt-8">
              <button @click="showEditGuest = false" class="flex-1 py-4 text-sm font-bold text-gray-400 hover:text-gray-600 transition-colors">Annuler</button>
              <button @click="saveEditGuest" :disabled="savingEdit || !editGuestData.first_name.trim() || !editGuestData.last_name.trim()"
                      class="flex-1 py-4 bg-primary-600 text-white rounded-2xl font-bold shadow-lg shadow-primary-600/30 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
                {{ savingEdit ? 'Enregistrement...' : 'Enregistrer' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ════ UpgradeModal ════ -->
    <UpgradeModal v-model="showUpgradeModal" />
  </div>
</template>

<style scoped>
.cursor-move { cursor: grab; }
.cursor-move:active { cursor: grabbing; }

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
