<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { getPlanInfo } from '../service/plans';
import { useToast } from '../composables/useToast';
import UpgradeModal from '../components/UpgradeModal.vue';

const { notifyError } = useToast();

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;
const auth = useAuthStore();

const guests = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const filterStatus = ref('all');

const planInfo = computed(() => getPlanInfo(auth.user?.plan || 'classic'));
const isPremium = computed(() => auth.user?.plan === 'premium');
const showAddGuest = ref(false);
const showUpgradeModal = ref(false);
const exportingCsv = ref(false);

// Export CSV de la liste d'invités — réservé au forfait Premium.
const exportCsv = async () => {
  if (!isPremium.value) { showUpgradeModal.value = true; return; }
  exportingCsv.value = true;
  try {
    const res = await api.get(`/guests/event/${eventId}/export/csv`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement('a');
    a.href = url;
    a.download = 'invites.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (err) {
    if (err.response?.status === 403 && !isPremium.value) showUpgradeModal.value = true;
    else notifyError(err, { fallback: "Erreur lors de l'export CSV." });
  } finally {
    exportingCsv.value = false;
  }
};

const newGuest = ref({
  first_name: '',
  last_name: '',
  email: '',
  rsvp_status: 'confirmed',
  plus_ones: 0,
  sub_guests: [],
  dietary_restrictions: '',
  message: ''
});

watch(() => newGuest.value.plus_ones, (newVal) => {
  const currentLen = newGuest.value.sub_guests.length;
  if (newVal > currentLen) {
    for (let i = 0; i < newVal - currentLen; i++) {
      newGuest.value.sub_guests.push({ first_name: '', last_name: '', dietary_restrictions: '' });
    }
  } else if (newVal < currentLen) {
    newGuest.value.sub_guests = newGuest.value.sub_guests.slice(0, newVal);
  }
});

const fetchGuests = async () => {
  try {
    loading.value = true;
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
    await api.post('/guests', { ...newGuest.value, event_id: parseInt(eventId) });
    showAddGuest.value = false;
    newGuest.value = { first_name: '', last_name: '', email: '', rsvp_status: 'confirmed', plus_ones: 0, sub_guests: [], dietary_restrictions: '', message: '' };
    fetchGuests();
  } catch (err) {
    notifyError(err, { fallback: "Erreur lors de l'ajout de l'invité." });
  }
};

const deleteGuest = async (id) => {
  if (!confirm("Supprimer cet invité ? S'il a des accompagnants, ils seront aussi supprimés.")) return;
  try {
    await api.delete(`/guests/${id}`);
    fetchGuests();
  } catch (err) {
    console.error("Erreur suppression", err);
  }
};

const updateGuestStatus = async (guestId, newStatus) => {
  try {
    await api.patch(`/guests/${guestId}`, { rsvp_status: newStatus });
    const guest = guests.value.find(g => g.id === guestId);
    if (guest) guest.rsvp_status = newStatus;
  } catch (err) {
    console.error("Erreur mise à jour statut", err);
  }
};

const sortedGuests = computed(() => {
  const mainGuests = guests.value.filter(g => !g.parent_id);
  const result = [];

  mainGuests.forEach(parent => {
    result.push({ ...parent, isChild: false });
    const children = guests.value.filter(g => g.parent_id === parent.id);
    children.forEach(child => {
      result.push({ ...child, isChild: true, parentName: parent.first_name });
    });
  });

  return result.filter(g => {
    const matchesSearch = `${g.first_name} ${g.last_name}`.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesFilter = filterStatus.value === 'all' || g.rsvp_status === filterStatus.value;
    return matchesSearch && matchesFilter;
  });
});

const stats = computed(() => {
  const main = guests.value.filter(g => !g.parent_id);
  return {
    total: main.length,
    confirmed: main.filter(g => g.rsvp_status === 'confirmed').length,
    declined: main.filter(g => g.rsvp_status === 'declined').length,
  };
});

// ── Dashboard RSVP temps réel (disponible pour tous) ─────────────────────
const rsvpDashboard = computed(() => {
  const all = guests.value;

  // Récap régimes alimentaires (tous invités confondus), agrégé par valeur.
  const diet = {};
  all.forEach(g => {
    const d = (g.dietary_restrictions || '').trim();
    if (d) diet[d] = (diet[d] || 0) + 1;
  });
  const dietary = Object.entries(diet)
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count);

  return {
    confirmed: stats.value.confirmed,
    declined: stats.value.declined,
    total: stats.value.confirmed + stats.value.declined,
    dietary,
  };
});

const statusLabel = { confirmed: 'Confirmé', declined: 'Absent' };
const statusClass = {
  confirmed: 'bg-green-100 text-green-700',
  declined:  'bg-red-100 text-red-700',
};

onMounted(fetchGuests);
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 font-sans">
    <nav class="bg-white border-b border-gray-200 min-h-16 py-2 flex items-center px-4 sm:px-8 sticky top-0 z-10 justify-between gap-2">
      <div class="flex items-center min-w-0">
        <button @click="router.push('/dashboard')" class="text-gray-400 hover:text-primary-600 mr-2 sm:mr-4 shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <h1 class="text-base sm:text-lg font-semibold text-gray-900 truncate">Gestion des Invités</h1>
      </div>
      <div class="flex space-x-2 sm:space-x-3 shrink-0">
        <!-- Export CSV — réservé Premium -->
        <button @click="exportCsv" :disabled="exportingCsv"
                :class="isPremium
                  ? 'border-gray-200 text-gray-700 hover:bg-gray-50'
                  : 'border-amber-200 text-amber-600 hover:bg-amber-50'"
                class="flex items-center gap-1.5 border bg-white px-3 sm:px-4 py-2 rounded-xl text-sm font-semibold transition-colors whitespace-nowrap disabled:opacity-50"
                :title="isPremium ? 'Exporter les invités en CSV' : 'Export CSV — Forfait Premium requis'">
          <span v-if="exportingCsv" class="w-4 h-4 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin"></span>
          <svg v-else-if="isPremium" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 1a5 5 0 00-5 5v3H6a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2v-8a2 2 0 00-2-2h-1V6a5 5 0 00-5-5zm3 8H9V6a3 3 0 016 0v3z"/></svg>
          <span class="hidden sm:inline">Export CSV</span>
        </button>
        <button @click="showAddGuest = true" class="bg-primary-600 text-white px-3 sm:px-6 py-2 rounded-xl text-sm font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20 whitespace-nowrap">
          + <span class="hidden sm:inline">Ajouter un Invité / Groupe</span><span class="sm:hidden">Invité</span>
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
      <!-- ═══ Dashboard RSVP temps réel ═══ -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6 mb-6 sm:mb-8">
        <div class="flex items-center justify-between mb-4 sm:mb-5">
          <h2 class="text-xs sm:text-sm font-black uppercase tracking-widest text-gray-700">Tableau de bord RSVP</h2>
          <span class="text-[9px] sm:text-[10px] font-bold uppercase tracking-widest text-primary-600 bg-primary-50 px-2 sm:px-2.5 py-1 rounded-full">Temps réel</span>
        </div>

        <!-- KPIs : 3 colonnes dès le mobile -->
        <div class="grid grid-cols-3 gap-2 sm:gap-3 mb-5 sm:mb-6">
          <div class="rounded-xl bg-green-50 border border-green-100 p-3 sm:p-4">
            <p class="text-[9px] sm:text-[10px] font-bold text-green-600 uppercase tracking-widest mb-1 leading-tight">Confirmés</p>
            <p class="text-xl sm:text-2xl font-black text-green-700">{{ rsvpDashboard.confirmed }}</p>
          </div>
          <div class="rounded-xl bg-red-50 border border-red-100 p-3 sm:p-4">
            <p class="text-[9px] sm:text-[10px] font-bold text-red-500 uppercase tracking-widest mb-1 leading-tight">Absents</p>
            <p class="text-xl sm:text-2xl font-black text-red-600">{{ rsvpDashboard.declined }}</p>
          </div>
          <div class="rounded-xl bg-gray-50 border border-gray-100 p-3 sm:p-4">
            <p class="text-[9px] sm:text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 leading-tight">Total</p>
            <p class="text-xl sm:text-2xl font-black text-gray-900">{{ rsvpDashboard.total }}</p>
          </div>
        </div>

        <!-- Récap régimes alimentaires -->
        <div>
          <p class="text-[9px] sm:text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Régimes alimentaires</p>
          <div v-if="rsvpDashboard.dietary.length" class="flex flex-wrap gap-2">
            <span v-for="d in rsvpDashboard.dietary" :key="d.label"
                  class="inline-flex items-center gap-1.5 bg-gray-100 text-gray-700 text-xs font-medium px-3 py-1.5 rounded-full">
              {{ d.label }}
              <span class="inline-flex items-center justify-center min-w-5 h-5 px-1 bg-white text-gray-900 text-[10px] font-bold rounded-full">{{ d.count }}</span>
            </span>
          </div>
          <p v-else class="text-xs text-gray-400 italic">Aucune contrainte alimentaire renseignée pour l'instant.</p>
        </div>
      </div>

      <!-- Filtres -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 mb-6 flex flex-col sm:flex-row gap-3">
        <input v-model="searchQuery" type="text" placeholder="Rechercher..." class="flex-1 px-4 py-2 border border-gray-100 bg-gray-50 rounded-xl text-sm outline-none focus:ring-2 focus:ring-primary-500">
        <select v-model="filterStatus" class="bg-gray-50 border border-gray-100 rounded-xl text-sm px-4 py-2">
          <option value="all">Tous les statuts</option>
          <option value="confirmed">Confirmés</option>
          <option value="declined">Absents</option>
        </select>
      </div>

      <!-- Liste -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-100">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Invité</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Type</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Statut</th>
              <th class="px-6 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Régime / Message</th>
              <th class="px-6 py-3 text-right text-[10px] font-bold text-gray-400 uppercase tracking-widest">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            <tr v-for="guest in sortedGuests" :key="guest.id" :class="guest.isChild ? 'bg-gray-50/30' : ''">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center" :class="guest.isChild ? 'ml-8' : ''">
                  <span v-if="guest.isChild" class="text-gray-300 mr-2">└─</span>
                  <div class="h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold mr-3"
                       :class="guest.isChild ? 'bg-gray-100 text-gray-500' : 'bg-primary-100 text-primary-700'">
                    {{ guest.first_name[0] }}{{ guest.last_name[0] }}
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ guest.first_name }} {{ guest.last_name }}</div>
                    <div v-if="!guest.isChild" class="text-[10px] text-gray-400">{{ guest.email || 'Pas d\'email' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-[10px] font-bold uppercase tracking-widest" :class="guest.isChild ? 'text-gray-400' : 'text-primary-500'">
                  {{ guest.isChild ? 'Accompagnant' : 'Principal' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <!-- Select inline pour modifier le statut -->
                <select
                  :value="guest.rsvp_status"
                  @change="updateGuestStatus(guest.id, $event.target.value)"
                  class="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border-0 outline-none cursor-pointer"
                  :class="statusClass[guest.rsvp_status] || 'bg-gray-100 text-gray-500'"
                >
                  <option value="confirmed">Confirmé</option>
                  <option value="declined">Absent</option>
                </select>
              </td>
              <td class="px-6 py-4">
                <p v-if="guest.dietary_restrictions" class="text-xs text-red-400">🍴 {{ guest.dietary_restrictions }}</p>
                <p v-if="guest.message" class="text-xs text-gray-500 italic">"{{ guest.message }}"</p>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <button @click="deleteGuest(guest.id)" class="text-gray-300 hover:text-red-500 transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </td>
            </tr>

            <tr v-if="!loading && sortedGuests.length === 0">
              <td colspan="5" class="px-6 py-16 text-center text-sm text-gray-400">Aucun invité trouvé.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal Ajout -->
    <div v-if="showAddGuest" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-[2.5rem] p-10 max-w-xl w-full shadow-2xl overflow-y-auto max-h-[90vh]">
        <h2 class="text-3xl font-serif text-gray-900 mb-8">Ajouter un Invité</h2>

        <div class="space-y-6">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Prénom</label>
              <input v-model="newGuest.first_name" type="text" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
            <div>
              <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Nom</label>
              <input v-model="newGuest.last_name" type="text" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Email (facultatif)</label>
              <input v-model="newGuest.email" type="email" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary-500 outline-none transition-all">
            </div>
            <div>
              <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Statut</label>
              <select v-model="newGuest.rsvp_status" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white outline-none">
                <option value="confirmed">Confirmé</option>
                <option value="declined">Absent</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Accompagnants</label>
            <select v-model.number="newGuest.plus_ones" class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white outline-none">
              <option v-for="n in 7" :key="n-1" :value="n-1">{{ n-1 === 0 ? 'Vient seul' : '+ ' + (n-1) + ' personnes' }}</option>
            </select>
          </div>

          <!-- Labels Dynamiques pour Accompagnants -->
          <div v-if="newGuest.plus_ones > 0" class="p-6 bg-primary-50/50 rounded-[2rem] border border-primary-100 space-y-4">
            <p class="text-[10px] font-black text-primary-600 uppercase tracking-widest mb-4">Noms des accompagnants</p>
            <div v-for="(sub, index) in newGuest.sub_guests" :key="index" class="grid grid-cols-2 gap-3">
              <input v-model="sub.first_name" type="text" :placeholder="'Prénom ' + (index+1)" class="px-4 py-3 rounded-xl border border-gray-100 text-sm outline-none focus:ring-1 focus:ring-primary-400">
              <input v-model="sub.last_name" type="text" :placeholder="'Nom ' + (index+1)" class="px-4 py-3 rounded-xl border border-gray-100 text-sm outline-none focus:ring-1 focus:ring-primary-400">
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">Régime alimentaire / Allergies</label>
            <input v-model="newGuest.dietary_restrictions" type="text" placeholder="Optionnel..." class="w-full px-5 py-4 rounded-2xl border border-gray-100 bg-gray-50 focus:bg-white outline-none">
          </div>
        </div>

        <div class="flex space-x-4 mt-10">
          <button @click="showAddGuest = false" class="flex-1 py-4 text-sm font-bold text-gray-400 hover:text-gray-600 transition-colors">Annuler</button>
          <button @click="addGuest" class="flex-1 py-4 bg-primary-600 text-white rounded-2xl font-bold hover:bg-primary-700 shadow-lg shadow-primary-600/30 transition-all">Enregistrer le groupe</button>
        </div>
      </div>
    </div>

    <!-- Modale d'upgrade (export CSV réservé Premium) -->
    <UpgradeModal v-model="showUpgradeModal" />
  </div>
</template>
