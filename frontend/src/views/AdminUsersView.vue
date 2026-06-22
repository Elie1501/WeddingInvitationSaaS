<script setup>
import { ref, onMounted } from 'vue';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { useToast } from '../composables/useToast';

const { notifyError } = useToast();

const users = ref([]);
const loading = ref(true);
const auth = useAuthStore();
const router = useRouter();

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/');
    users.value = response.data;
  } catch (err) {
    console.error("Erreur lors de la récupération des utilisateurs", err);
    const status = err.response?.status;
    if (status === 403) {
      notifyError("Accès refusé : vous n'êtes pas administrateur.");
      router.push('/dashboard');
    } else if (status === 401 || status === 404) {
      auth.logout();
      router.push('/login');
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
    notifyError(err, { fallback: "Erreur lors de la modification du statut." });
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
    notifyError(err, { fallback: "Erreur lors de la suppression." });
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
            <h1 class="text-2xl text-primary-800">Administration — Utilisateurs</h1>
          </div>
          <div class="flex items-center">
            <button
              @click="router.push('/admin/stats')"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-700 hover:bg-primary-50 rounded-lg transition-colors border border-primary-200"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
              Statistiques
            </button>
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
                  <template v-if="user.id !== auth.user?.id">
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
                  </template>
                  <span v-else class="text-xs text-gray-400 italic">Mon compte</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

  </div>
</template>
