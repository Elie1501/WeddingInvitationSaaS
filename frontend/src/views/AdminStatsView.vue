<script setup>
import { ref, onMounted } from 'vue';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const stats = ref(null);
const loading = ref(true);
const auth = useAuthStore();
const router = useRouter();

const fetchStats = async () => {
  try {
    const response = await api.get('/users/stats');
    stats.value = response.data;
  } catch (err) {
    const status = err.response?.status;
    if (status === 403) {
      router.push('/dashboard');
    } else if (status === 401 || status === 404) {
      auth.logout();
      router.push('/login');
    }
  } finally {
    loading.value = false;
  }
};

const fmt = (n) => new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
const currentMonth = new Date().toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });

onMounted(fetchStats);
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
            <h1 class="text-2xl text-primary-800">Administration — Statistiques</h1>
          </div>
          <div class="flex items-center">
            <button
              @click="router.push('/admin/users')"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-700 hover:bg-primary-50 rounded-lg transition-colors border border-primary-200"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
              Utilisateurs
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">

      <div v-if="loading" class="flex justify-center items-center py-40">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>

      <div v-else-if="stats" class="space-y-10">

        <!-- Revenus -->
        <section>
          <p class="text-xs font-bold uppercase tracking-widest text-primary-400 mb-4">Revenus — {{ currentMonth }}</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">MRR</span>
                <div class="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
              </div>
              <p class="text-4xl font-light text-gray-900">{{ fmt(stats.mrr) }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans">{{ stats.new_users_this_month }} nouveaux inscrits ce mois</p>
            </div>

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">ARR (projection)</span>
                <div class="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                </div>
              </div>
              <p class="text-4xl font-light text-gray-900">{{ fmt(stats.arr) }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans">MRR × 12 mois</p>
            </div>

          </div>
        </section>

        <!-- Utilisateurs -->
        <section>
          <p class="text-xs font-bold uppercase tracking-widest text-primary-400 mb-4">Utilisateurs</p>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Total inscrits</span>
                <div class="w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.total_users }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans">+{{ stats.new_users_this_month }} ce mois</p>
            </div>

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Forfait Premium</span>
                <div class="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-amber-600" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.premium_users }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans">
                {{ stats.total_users > 0 ? Math.round(stats.premium_users / stats.total_users * 100) : 0 }}% des inscrits
              </p>
            </div>

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Forfait Classic</span>
                <div class="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.classic_users }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans">
                {{ stats.total_users > 0 ? Math.round(stats.classic_users / stats.total_users * 100) : 0 }}% des inscrits
              </p>
            </div>

          </div>
        </section>

        <!-- Conversion & Rétention -->
        <section>
          <p class="text-xs font-bold uppercase tracking-widest text-primary-400 mb-4">Conversion & Rétention</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Taux de conversion</span>
                <div class="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.conversion_rate }}<span class="text-2xl text-gray-400">%</span></p>
              <p class="text-xs text-gray-400 mt-3 mb-2 font-sans">Inscrits → Premium</p>
              <div class="w-full bg-gray-100 rounded-full h-1.5">
                <div
                  class="bg-blue-500 h-1.5 rounded-full transition-all"
                  :style="{ width: Math.min(stats.conversion_rate, 100) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Churn rate</span>
                <div class="w-10 h-10 rounded-xl bg-red-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.churn_rate }}<span class="text-2xl text-gray-400">%</span></p>
              <p class="text-xs text-gray-400 mt-3 mb-2 font-sans">Comptes désactivés</p>
              <div class="w-full bg-gray-100 rounded-full h-1.5">
                <div
                  class="bg-red-400 h-1.5 rounded-full transition-all"
                  :style="{ width: Math.min(stats.churn_rate, 100) + '%' }"
                ></div>
              </div>
            </div>

          </div>
        </section>

        <!-- Activité -->
        <section>
          <p class="text-xs font-bold uppercase tracking-widest text-primary-400 mb-4">Activité</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">

            <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-8">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold uppercase tracking-widest text-gray-400">Cartes créées ce mois</span>
                <div class="w-10 h-10 rounded-xl bg-violet-100 flex items-center justify-center">
                  <svg class="w-5 h-5 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
              </div>
              <p class="text-5xl font-light text-gray-900">{{ stats.cards_this_month }}</p>
              <p class="text-xs text-gray-400 mt-2 font-sans capitalize">{{ currentMonth }}</p>
            </div>

          </div>
        </section>

      </div>
    </main>
  </div>
</template>
