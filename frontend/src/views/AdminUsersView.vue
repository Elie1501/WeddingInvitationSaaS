<script setup>
import { ref, onMounted } from 'vue';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const users = ref([]);
const loading = ref(true);
const auth = useAuthStore();
const router = useRouter();

const selectedUser = ref(null);
const userCards = ref([]);
const loadingCards = ref(false);
const showCardsModal = ref(false);

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/');
    users.value = response.data;
  } catch (err) {
    console.error("Erreur lors de la récupération des utilisateurs", err);
    if (err.response?.status === 403) {
      alert("Accès refusé : vous n'êtes pas administrateur.");
      router.push('/dashboard');
    }
  } finally {
    loading.value = false;
  }
};

const toggleUserStatus = async (user) => {
  try {
    const newStatus = !user.is_active;
    const response = await api.patch(`/users/${user.id}/status`, { is_active: newStatus });
    // Mettre à jour localement
    user.is_active = response.data.is_active;
  } catch (err) {
    console.error("Erreur lors de la modification du statut", err);
    alert(err.response?.data?.detail || "Erreur lors de la modification du statut.");
  }
};

const deleteUser = async (userId) => {
  if (!confirm("Êtes-vous sûr de vouloir supprimer définitivement cet utilisateur ? Cette action est irréversible.")) {
    return;
  }
  try {
    await api.delete(`/users/${userId}`);
    // Mettre à jour la liste localement
    users.value = users.value.filter(u => u.id !== userId);
  } catch (err) {
    console.error("Erreur lors de la suppression", err);
    alert(err.response?.data?.detail || "Erreur lors de la suppression.");
  }
};

const openUserCards = async (user) => {
  selectedUser.value = user;
  showCardsModal.value = true;
  loadingCards.value = true;
  userCards.value = [];
  try {
    const response = await api.get(`/users/${user.id}/cards`);
    userCards.value = response.data;
  } catch (err) {
    console.error("Erreur lors du chargement des cartes", err);
  } finally {
    loadingCards.value = false;
  }
};

onMounted(() => {
  if (!auth.user?.is_admin) {
    // Double vérification côté client
    fetchUsers();
  } else {
    fetchUsers();
  }
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 pb-20">
    <nav class="bg-white border-b border-primary-100 sticky top-0 z-50 shadow-sm shadow-primary-900/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20">
          <div class="flex items-center">
            <button @click="router.push('/dashboard')" class="mr-4 text-primary-600 hover:text-primary-800 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            </button>
            <h1 class="text-2xl text-primary-800">Administration - Utilisateurs</h1>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">
      <div class="bg-white rounded-2xl shadow-sm border border-primary-100 overflow-hidden">
        <div class="p-8 border-b border-primary-50">
          <h2 class="text-xl text-gray-900 font-medium">Liste des inscrits</h2>
          <p class="text-sm text-gray-500 font-sans mt-1">Gérez et visualisez l'ensemble des utilisateurs de la plateforme.</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-20">
           <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left font-sans">
            <thead>
              <tr class="bg-primary-50/50 text-primary-800 text-xs uppercase tracking-widest font-bold">
                <th class="px-8 py-4">ID</th>
                <th class="px-8 py-4">Utilisateur</th>
                <th class="px-8 py-4">Forfait</th>
                <th class="px-8 py-4">Rôle</th>
                <th class="px-8 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-primary-50">
              <tr v-for="user in users" :key="user.id" class="hover:bg-primary-50/30 transition-colors">
                <td class="px-8 py-4 text-gray-400 text-sm font-mono">#{{ user.id }}</td>
                <td class="px-8 py-4">
                  <div class="flex flex-col">
                    <span class="text-gray-900 font-medium">{{ user.email }}</span>
                  </div>
                </td>
                <td class="px-8 py-4">
                  <span 
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider"
                    :class="user.plan === 'premium' ? 'bg-primary-100 text-primary-800' : 'bg-gray-100 text-gray-600'"
                  >
                    {{ user.plan }}
                  </span>
                </td>
                <td class="px-8 py-4">
                  <span v-if="user.is_admin" class="text-amber-600 text-xs font-bold uppercase flex items-center">
                    <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    Admin
                  </span>
                  <span v-else class="text-gray-400 text-xs uppercase">Client</span>
                </td>
                <td class="px-8 py-4 text-right space-x-4">
                  <button 
                    @click="openUserCards(user)"
                    class="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
                  >
                    Cartes
                  </button>
                  <button 
                    @click="toggleUserStatus(user)"
                    :class="user.is_active ? 'text-amber-600 hover:text-amber-800' : 'text-green-600 hover:text-green-800'"
                    class="text-sm font-medium transition-colors"
                  >
                    {{ user.is_active ? 'Désactiver' : 'Activer' }}
                  </button>
                  <button 
                    @click="deleteUser(user.id)"
                    class="text-red-600 hover:text-red-800 text-sm font-medium transition-colors"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Modal Cartes Utilisateur -->
    <div v-if="showCardsModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-4xl w-full shadow-2xl max-h-[90vh] flex flex-col">
        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="text-2xl text-gray-900">Cartes de {{ selectedUser?.email }}</h2>
            <p class="text-sm text-gray-500 font-sans mt-1">Aperçu visuel des invitations créées.</p>
          </div>
          <button @click="showCardsModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div v-if="loadingCards" class="flex justify-center items-center py-20 flex-grow">
           <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>

        <div v-else-if="userCards.length === 0" class="py-20 text-center flex-grow">
           <p class="text-gray-500 italic">Cet utilisateur n'a pas encore créé de carte.</p>
        </div>

        <div v-else class="overflow-y-auto pr-2 flex-grow">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="card in userCards" :key="card.id" class="border border-primary-100 rounded-2xl p-6 hover:shadow-md transition-shadow bg-primary-50/20">
              <div class="flex justify-between items-start mb-4">
                <span 
                  class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-widest"
                  :class="card.is_published ? 'bg-secondary-100 text-secondary-800' : 'bg-gray-200 text-gray-600'"
                >
                  {{ card.is_published ? 'Publiée' : 'Brouillon' }}
                </span>
                <span class="text-xs text-gray-400 font-mono">ID: #{{ card.id }}</span>
              </div>
              
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ card.slug || 'Sans nom' }}</h3>
              
              <div class="space-y-4">
                <a 
                  v-if="card.is_published"
                  :href="'/cards/' + card.slug" 
                  target="_blank"
                  class="block w-full text-center py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors shadow-sm shadow-primary-600/20"
                >
                  Voir le rendu visuel
                </a>
                <span v-else class="block w-full text-center py-2 bg-gray-100 text-gray-400 rounded-lg text-sm font-medium cursor-not-allowed">
                  Non publiée
                </span>
                <div class="pt-4 border-t border-primary-50">
                   <p class="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-2">Détails techniques</p>
                   <div class="space-y-1 text-xs text-gray-600 font-sans">
                      <p><strong>Template:</strong> {{ card.template_id }}</p>
                      <p><strong>Version:</strong> {{ card.current_version }}</p>
                      <p><strong>Slug:</strong> {{ card.slug }}</p>
                   </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button @click="showCardsModal = false" class="w-full mt-8 py-3 bg-gray-100 text-gray-800 rounded-xl font-semibold hover:bg-gray-200 transition-colors">Fermer</button>
      </div>
    </div>
  </div>
</template>
