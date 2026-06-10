<script setup>
import { ref, computed, onMounted } from 'vue';
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
    const s = err.response?.status;
    if (s === 403) router.push('/dashboard');
    else if (s === 401 || s === 404) { auth.logout(); router.push('/login'); }
  } finally {
    loading.value = false;
  }
};

const fmt = (n) =>
  new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
const currentMonth = new Date().toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });

// ── Donut (r=40, cx=50, cy=50, viewBox 100×100) ───────────────────────
const CIRC = 2 * Math.PI * 40; // ≈ 251.3

const premiumArc = computed(() => {
  const t = stats.value?.total_users || 0;
  if (t === 0) return { d: `0 ${CIRC}`, offset: 0 };
  const len = (stats.value.premium_users / t) * CIRC;
  return { d: `${len} ${CIRC}`, offset: 0 };
});

const classicArc = computed(() => {
  const t = stats.value?.total_users || 0;
  if (t === 0) return { d: `0 ${CIRC}`, offset: 0 };
  const premLen = (stats.value.premium_users / t) * CIRC;
  const classLen = (stats.value.classic_users / t) * CIRC;
  return { d: `${classLen} ${CIRC}`, offset: -premLen };
});

// ── Jauge demi-cercle (cx=60, cy=65, r=50, viewBox 120×70) ─────────────
// Track : M 10 65 A 50 50 0 0 0 110 65  (sweep=0 = sens anti-horaire = passe par le haut)
const gaugeArc = (value) => {
  if (!value || value <= 0) return null;
  const v = Math.min(value, 99.99);
  const rad = (180 - (v / 100) * 180) * (Math.PI / 180);
  const ex = (60 + 50 * Math.cos(rad)).toFixed(2);
  const ey = (65 - 50 * Math.sin(rad)).toFixed(2);
  return `M 10 65 A 50 50 0 0 0 ${ex} ${ey}`;
};

onMounted(fetchStats);
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-24">

    <!-- Nav -->
    <nav class="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="router.push('/dashboard')" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
          </button>
          <div>
            <span class="font-semibold text-gray-900">Tableau de bord</span>
            <span class="ml-2 text-xs text-gray-400 capitalize">{{ currentMonth }}</span>
          </div>
        </div>
        <button @click="router.push('/admin/users')"
          class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          Utilisateurs
        </button>
      </div>
    </nav>

    <main class="max-w-6xl mx-auto px-6 mt-8 space-y-6">

      <!-- Loader -->
      <div v-if="loading" class="flex justify-center items-center py-40">
        <div class="w-8 h-8 border-2 border-indigo-300 border-t-indigo-600 rounded-full animate-spin"></div>
      </div>

      <template v-else-if="stats">

        <!-- Ligne 1 : 4 chiffres clés -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

          <div class="bg-white rounded-2xl p-5 border border-gray-100">
            <p class="text-xs text-gray-400 mb-1">MRR</p>
            <p class="text-2xl font-semibold text-gray-900">{{ fmt(stats.mrr) }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ stats.new_users_this_month }} nouveaux ce mois</p>
          </div>

          <div class="bg-white rounded-2xl p-5 border border-gray-100">
            <p class="text-xs text-gray-400 mb-1">ARR projeté</p>
            <p class="text-2xl font-semibold text-gray-900">{{ fmt(stats.arr) }}</p>
            <p class="text-xs text-gray-400 mt-1">MRR × 12 mois</p>
          </div>

          <div class="bg-white rounded-2xl p-5 border border-gray-100">
            <p class="text-xs text-gray-400 mb-1">Cartes créées</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.cards_this_month }}</p>
            <p class="text-xs text-gray-400 mt-1 capitalize">{{ currentMonth }}</p>
          </div>

          <div class="bg-white rounded-2xl p-5 border border-gray-100">
            <p class="text-xs text-gray-400 mb-1">Inscrits actifs</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.total_users }}</p>
            <p class="text-xs text-gray-400 mt-1">+{{ stats.new_users_this_month }} ce mois</p>
          </div>

        </div>

        <!-- Ligne 2 : Donut + Jauges -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

          <!-- Donut : répartition forfaits -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100">
            <p class="text-sm font-semibold text-gray-800 mb-1">Répartition des forfaits</p>
            <p class="text-xs text-gray-400 mb-4">{{ stats.total_users }} inscrits actifs</p>

            <div class="flex items-center justify-center">
              <svg viewBox="0 0 100 100" class="w-44 h-44">
                <!-- Track gris -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#F3F4F6" stroke-width="14"
                  transform="rotate(-90, 50, 50)" />
                <!-- Classic (gris) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#D1D5DB" stroke-width="14"
                  :stroke-dasharray="classicArc.d"
                  :stroke-dashoffset="classicArc.offset"
                  stroke-linecap="butt"
                  transform="rotate(-90, 50, 50)" />
                <!-- Premium (amber) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#F59E0B" stroke-width="14"
                  :stroke-dasharray="premiumArc.d"
                  :stroke-dashoffset="premiumArc.offset"
                  stroke-linecap="butt"
                  transform="rotate(-90, 50, 50)" />
                <!-- Centre -->
                <text x="50" y="46" text-anchor="middle" font-size="18" font-weight="600" fill="#111827">
                  {{ stats.total_users }}
                </text>
                <text x="50" y="58" text-anchor="middle" font-size="8" fill="#9CA3AF">inscrits</text>
              </svg>
            </div>

            <div class="flex justify-around mt-3">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-amber-400 inline-block"></span>
                <div>
                  <p class="text-base font-semibold text-gray-900">{{ stats.premium_users }}</p>
                  <p class="text-xs text-gray-400">Premium</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-gray-300 inline-block"></span>
                <div>
                  <p class="text-base font-semibold text-gray-900">{{ stats.classic_users }}</p>
                  <p class="text-xs text-gray-400">Classic</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Jauge : taux de conversion -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100">
            <p class="text-sm font-semibold text-gray-800 mb-1">Taux de conversion</p>
            <p class="text-xs text-gray-400 mb-2">Inscrits → Premium</p>

            <div class="flex items-center justify-center mt-2">
              <svg viewBox="0 0 120 70" class="w-52 h-32">
                <!-- Track -->
                <path d="M 10 65 A 50 50 0 0 0 110 65"
                  fill="none" stroke="#EEF2FF" stroke-width="10" stroke-linecap="round" />
                <!-- Valeur -->
                <path v-if="gaugeArc(stats.conversion_rate)"
                  :d="gaugeArc(stats.conversion_rate)"
                  fill="none" stroke="#6366F1" stroke-width="10" stroke-linecap="round" />
                <!-- Chiffre -->
                <text x="60" y="60" text-anchor="middle" font-size="20" font-weight="600" fill="#111827">
                  {{ stats.conversion_rate }}%
                </text>
              </svg>
            </div>

            <div class="mt-2 text-center">
              <p class="text-xs text-gray-400">
                {{ stats.premium_users }} utilisateurs sur {{ stats.total_users }} ont choisi Premium
              </p>
            </div>
          </div>

          <!-- Jauge : churn rate -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100">
            <p class="text-sm font-semibold text-gray-800 mb-1">Churn rate</p>
            <p class="text-xs text-gray-400 mb-2">Comptes désactivés</p>

            <div class="flex items-center justify-center mt-2">
              <svg viewBox="0 0 120 70" class="w-52 h-32">
                <!-- Track -->
                <path d="M 10 65 A 50 50 0 0 0 110 65"
                  fill="none" stroke="#FEF2F2" stroke-width="10" stroke-linecap="round" />
                <!-- Valeur -->
                <path v-if="gaugeArc(stats.churn_rate)"
                  :d="gaugeArc(stats.churn_rate)"
                  fill="none" stroke="#F87171" stroke-width="10" stroke-linecap="round" />
                <!-- Chiffre -->
                <text x="60" y="60" text-anchor="middle" font-size="20" font-weight="600" fill="#111827">
                  {{ stats.churn_rate }}%
                </text>
              </svg>
            </div>

            <div class="mt-2 text-center">
              <p class="text-xs text-gray-400">
                Approximation basée sur les comptes inactifs
              </p>
            </div>
          </div>

        </div>

      </template>
    </main>
  </div>
</template>
