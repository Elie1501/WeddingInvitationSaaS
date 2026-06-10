<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { useRouter, useRoute } from 'vue-router';
import { getPlanInfo } from '../service/plans';

const events = ref([]);
const loading = ref(true);
const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const baseUrl = window.location.origin;

const planInfo = computed(() => getPlanInfo(auth.user?.plan || 'classic'));
const showApiModal = ref(false);
const showPlanModal = ref(false);
const planUpdateLoading = ref(false);
const canCreateEvent = computed(() => events.value.length < planInfo.value.max_sites);

// ─── Delete modal ──────────────────────────────────────────────────────────
const deleteModal = ref({ show: false, eventId: null, eventTitle: '' });

const handleDeleteEvent = (eventId, eventTitle) => {
  deleteModal.value = { show: true, eventId, eventTitle };
};

const confirmDelete = async () => {
  const eventId = deleteModal.value.eventId;
  deleteModal.value = { show: false, eventId: null, eventTitle: '' };
  try {
    await api.delete(`/events/${eventId}`);
    events.value = events.value.filter(e => e.id !== eventId);
  } catch {
    alert('Erreur lors de la suppression de l\'événement.');
  }
};

// ─── Publish / Depublish ───────────────────────────────────────────────────
const togglePublish = async (cardId) => {
  try {
    const res = await api.post(`/cards/${cardId}/publish`);
    const ev = events.value.find(e => e.card?.id === cardId);
    if (ev?.card) ev.card.is_published = res.data.is_published;
  } catch {
    alert('Erreur lors de la mise à jour du statut de publication.');
  }
};

// ─── Misc ──────────────────────────────────────────────────────────────────
const handleCreateEvent = () => {
  if (!canCreateEvent.value) { showPlanModal.value = true; return; }
  router.push('/events/create');
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    alert('Lien copié dans le presse-papier !');
  } catch {
    console.error('Erreur lors de la copie');
  }
};

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};

const handleUpdatePlan = async (newPlan) => {
  try {
    planUpdateLoading.value = true;
    const res = await api.post('/payments/create-checkout-session', { plan_name: newPlan });
    if (res.data.checkout_url) window.location.href = res.data.checkout_url;
  } catch {
    alert('Impossible d\'initialiser le paiement. Veuillez réessayer.');
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

onMounted(async () => {
  if (!auth.user) await auth.fetchMe();

  const sessionId = route.query.session_id;
  const paymentSuccess = route.query.payment_success;
  if (paymentSuccess === 'true' && sessionId) {
    try {
      await api.post('/payments/confirm-payment', { session_id: sessionId });
      await auth.fetchMe();
      router.replace({ query: {} });
    } catch { /* silent */ }
  }

  try {
    const res = await api.get('/events/');
    events.value = res.data;
  } catch { /* silent */ } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 pb-20">

    <!-- ── Navbar ── -->
    <nav class="bg-white border-b border-primary-100 sticky top-0 z-50 shadow-sm shadow-primary-900/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20">

          <div class="flex items-center">
            <h1 class="text-2xl text-primary-800">Saas Wedding</h1>
          </div>

          <div class="flex items-center gap-4">
            <button
              v-if="auth.user?.is_admin"
              @click="router.push('/admin/users')"
              class="bg-amber-50 text-amber-700 border border-amber-200 px-4 py-2 rounded-full text-xs font-bold uppercase tracking-widest hover:bg-amber-100 transition-colors"
            >
              Panel Admin
            </button>

            <!-- User info + plan modifier -->
            <div v-if="auth.user" class="flex flex-col items-end">
              <span class="text-gray-900 font-sans text-sm font-medium">{{ auth.user.email }}</span>
              <div class="flex items-center gap-1.5">
                <span
                  :class="auth.user.plan === 'premium' ? 'text-primary-600' : 'text-gray-500'"
                  class="text-[10px] font-bold uppercase tracking-widest"
                >{{ planInfo.name }}</span>
                <!-- Pencil icon — modifier le forfait -->
                <button
                  @click="showPlanModal = true"
                  title="Modifier le forfait"
                  aria-label="Modifier le forfait"
                  class="text-primary-400 hover:text-primary-600 transition-colors p-0.5 rounded"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Logout button -->
            <button
              @click="handleLogout"
              class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border border-gray-200 text-gray-600
                     hover:border-red-200 hover:text-red-600 hover:bg-red-50 transition-all text-sm font-medium font-sans"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              Déconnexion
            </button>
          </div>

        </div>
      </div>
    </nav>

    <!-- ── Main ── -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">

      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-12">
        <div>
          <h2 class="text-4xl text-gray-900 mb-2">Mes Événements</h2>
          <p class="text-gray-500 font-sans">Gérez vos invitations, listes d'invités et plans de table avec élégance.</p>
        </div>
        <button
          @click="handleCreateEvent"
          :class="canCreateEvent ? 'bg-primary-600 hover:bg-primary-700' : 'bg-gray-300 cursor-not-allowed'"
          class="mt-6 md:mt-0 inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-full text-white shadow-md transition-all duration-300 font-sans"
          :title="!canCreateEvent ? `Limite atteinte — forfait ${planInfo.name} : ${planInfo.max_sites} site(s) max` : ''"
        >
          <svg v-if="canCreateEvent" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          <svg v-else class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
          </svg>
          {{ canCreateEvent ? 'Créer un événement' : 'Limite atteinte — Passer au Premium' }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>

      <!-- Grid d'événements -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="event in events" :key="event.id"
          class="bg-white rounded-2xl p-8 shadow-sm shadow-primary-900/5 border border-primary-100
                 hover:shadow-lg hover:shadow-primary-900/10 transition-all duration-300 group flex flex-col h-full"
        >

          <div class="flex-grow">
            <!-- Status badge -->
            <div class="flex justify-between items-start mb-6">
              <span
                class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold font-sans tracking-wide"
                :class="event.card?.is_published
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-500'"
              >
                <span
                  class="text-[10px]"
                  :class="event.card?.is_published ? 'text-green-500' : 'text-gray-400'"
                >{{ event.card?.is_published ? '●' : '○' }}</span>
                {{ event.card?.is_published ? 'En ligne' : 'Hors ligne' }}
              </span>
            </div>

            <h3 class="text-2xl text-gray-900 mb-4 group-hover:text-primary-700 transition-colors">{{ event.title }}</h3>

            <div class="space-y-3 font-sans text-gray-600 text-sm">
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-3 text-primary-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                {{ event.date ? new Date(event.date).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) : '—' }}
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-3 text-primary-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                {{ event.location || '—' }}
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="mt-8 pt-6 border-t border-gray-100 flex flex-col space-y-3 font-sans">

            <button
              @click="event.card ? $router.push(`/cards/edit/${event.card.id}`) : null"
              class="w-full py-2.5 px-4 bg-primary-50 hover:bg-primary-100 text-primary-800 rounded-lg text-sm font-medium transition-colors border border-primary-200"
            >
              Éditer l'invitation
            </button>

            <!-- Mettre en ligne / Dépublier -->
            <button
              v-if="event.card && !event.card.is_published"
              @click="togglePublish(event.card.id)"
              class="w-full py-2.5 px-4 bg-green-50 hover:bg-green-100 text-green-700 rounded-lg text-sm font-medium transition-colors border border-green-200 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12l5 5L20 7"/>
              </svg>
              Mettre en ligne
            </button>
            <button
              v-if="event.card?.is_published"
              @click="togglePublish(event.card.id)"
              class="w-full py-2.5 px-4 bg-gray-50 hover:bg-gray-100 text-gray-600 rounded-lg text-sm font-medium transition-colors border border-gray-200 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
              </svg>
              Dépublier
            </button>

            <button
              @click="$router.push(`/events/${event.id}/guests`)"
              class="w-full py-2.5 px-4 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200 shadow-sm"
            >
              Gérer les invités (RSVP)
            </button>

            <button
              @click="goToTables(event.id)"
              :class="!planInfo.can_use_tables ? 'opacity-50 grayscale cursor-not-allowed' : ''"
              class="w-full py-2.5 px-4 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200 shadow-sm flex items-center justify-center"
            >
              Plan de table
              <svg v-if="!planInfo.can_use_tables" class="w-3.5 h-3.5 ml-2 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
              </svg>
            </button>

            <button
              @click="handleDeleteEvent(event.id, event.title)"
              class="w-full py-2.5 px-4 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg text-sm font-medium transition-colors border border-red-100 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              Supprimer l'événement
            </button>

            <!-- Share section -->
            <div v-if="event.card?.is_published" class="pt-4 mt-2 border-t border-gray-50">
              <p class="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-3">Partager l'invitation</p>
              <div class="flex items-center gap-2">
                <div class="flex-grow bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-xs font-mono text-gray-500 truncate">
                  {{ baseUrl }}/cards/{{ event.card.slug }}
                </div>
                <button
                  @click="copyToClipboard(`${baseUrl}/cards/${event.card.slug}`)"
                  class="p-2 bg-white border border-gray-200 rounded-lg text-primary-600 hover:bg-primary-50 transition-colors shadow-sm"
                  title="Copier le lien"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
                  </svg>
                </button>
                <a
                  :href="'https://wa.me/?text=' + encodeURIComponent('Découvrez notre invitation de mariage : ' + baseUrl + '/cards/' + event.card.slug)"
                  target="_blank"
                  class="p-2 bg-white border border-gray-200 rounded-lg text-green-600 hover:bg-green-50 transition-colors shadow-sm"
                  title="Partager sur WhatsApp"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                </a>
              </div>
            </div>
            <div v-else class="pt-2 text-center">
              <span class="text-[10px] text-gray-400 italic">Publiez votre invitation pour obtenir le lien de partage</span>
            </div>

          </div>
        </div>
      </div>
    </main>

    <!-- ── Modale confirmation suppression ── -->
    <Transition name="modal-fade">
      <div
        v-if="deleteModal.show"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[200] flex items-center justify-center p-4"
        @click.self="deleteModal.show = false"
      >
        <div class="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl">
          <div class="flex items-start gap-4 mb-5">
            <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Supprimer l'événement</h3>
              <p class="text-sm text-gray-500 mt-1">
                <span class="font-semibold text-gray-700">« {{ deleteModal.eventTitle }} »</span>
              </p>
            </div>
          </div>
          <p class="text-sm text-gray-600 leading-relaxed bg-red-50 border border-red-100 rounded-xl p-4">
            Cette action supprimera <strong>définitivement</strong> l'invitation et son lien public.
            Les invités, les RSVP et le plan de table associés seront également supprimés.
            <strong>Cette opération est irréversible.</strong>
          </p>
          <div class="flex gap-3 mt-6">
            <button
              @click="deleteModal.show = false"
              class="flex-1 py-2.5 rounded-xl border border-gray-200 text-gray-700 text-sm font-medium hover:bg-gray-50 transition-colors"
            >
              Annuler
            </button>
            <button
              @click="confirmDelete"
              class="flex-1 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition-colors"
            >
              Supprimer définitivement
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ── Modale Forfait ── -->
    <div v-if="showPlanModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-xl w-full shadow-2xl">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-2xl text-gray-900">Gérer mon forfait</h2>
          <button @click="showPlanModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Classic -->
          <div class="border-2 rounded-2xl p-6 transition-all"
               :class="auth.user.plan === 'classic' ? 'border-primary-600 bg-primary-50' : 'border-gray-100 hover:border-primary-200'">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="font-bold text-lg text-gray-900">Classic</h3>
                <span class="text-primary-600 font-bold text-sm">29 €</span>
              </div>
              <span v-if="auth.user.plan === 'classic'" class="bg-primary-600 text-white text-[10px] px-2 py-0.5 rounded-full uppercase tracking-widest">Actuel</span>
            </div>
            <ul class="text-sm text-gray-600 space-y-2 mb-6 font-sans">
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Plan de table complet</li>
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> 1 site d'invitation</li>
            </ul>
            <button
              v-if="auth.user.plan !== 'classic'"
              @click="handleUpdatePlan('classic')"
              :disabled="planUpdateLoading"
              class="w-full py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg text-sm font-medium transition-colors"
            >Choisir Classic</button>
          </div>
          <!-- Premium -->
          <div class="border-2 rounded-2xl p-6 transition-all"
               :class="auth.user.plan === 'premium' ? 'border-primary-600 bg-primary-50' : 'border-gray-100 hover:border-primary-200'">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="font-bold text-lg text-gray-900">Premium</h3>
                <span class="text-primary-600 font-bold text-sm">79 €</span>
              </div>
              <span v-if="auth.user.plan === 'premium'" class="bg-primary-600 text-white text-[10px] px-2 py-0.5 rounded-full uppercase tracking-widest">Actuel</span>
            </div>
            <ul class="text-sm text-gray-600 space-y-2 mb-6 font-sans">
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> 5 sites d'invitation</li>
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Import/Export CSV</li>
            </ul>
            <button
              v-if="auth.user.plan !== 'premium'"
              @click="handleUpdatePlan('premium')"
              :disabled="planUpdateLoading"
              class="w-full py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors shadow-md shadow-primary-600/20"
            >Passer en Premium</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.15s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
