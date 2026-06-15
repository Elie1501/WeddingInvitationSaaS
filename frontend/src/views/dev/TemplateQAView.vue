<!--
  TemplateQAView.vue — Phase 4 : filet de sécurité + banc de test des couleurs (READ-ONLY)
  ============================================================================
  - Affiche tous les templates en cadre mobile (390px) avec bord rouge → repère les overflow.
  - Banc de test : injecte les 5 CSS vars sur chaque carte. Un template qui réagit
    lit bien les variables ; un template qui ne bouge pas a des couleurs hardcodées.
-->
<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { DEMO_CONFIGS } from '@/data/demoConfigs';
import CardRenderer from '@/components/card/CardRenderer.vue';

// Mock complet : on met des sous-événements pour que le Programme s'affiche
// (sinon impossible de tester --color-section-title dessus).
const mockEvent = {
  groom_name: 'Elie',
  bride_name: 'Sarah',
  date: '2026-06-25T15:00:00',
  location: 'Saint-Tropez',
  address: 'Saint-Tropez, France',
  sub_events: [
    { time: '15h00', title: 'Cérémonie',      location: 'Église du village' },
    { time: '17h00', title: 'Cocktail',        location: 'Les Jardins' },
    { time: '20h00', title: 'Dîner & Soirée', location: 'Villa Sunset' },
  ],
};

const entries = Object.entries(DEMO_CONFIGS);

// ── Banc de test des 5 variables de couleur ────────────────────────────────
const active = ref(false);
const vars = ref({
  '--color-names':         '#E11D74',
  '--color-countdown':     '#0FB5AE',
  '--color-section-title': '#7C3AED',
  '--color-text':          '#2563EB',
  '--color-bg':            '#FFF3E0',
});
const labels = {
  '--color-names':         'Noms',
  '--color-countdown':     'Compte à rebours',
  '--color-section-title': 'Titres de section',
  '--color-text':          'Textes',
  '--color-bg':            'Fond',
};

// On force les vars via une <style> dynamique ciblant .card-engine (là où
// CardRenderer définit ses propres vars), avec !important pour primer sur le défaut.
let styleEl = null;
function applyOverrides() {
  if (!styleEl) return;
  if (!active.value) { styleEl.textContent = ''; return; }
  const decls = Object.entries(vars.value)
    .map(([k, v]) => `${k}: ${v} !important;`)
    .join(' ');
  styleEl.textContent = `.qa-board .card-engine { ${decls} }`;
}

onMounted(() => {
  styleEl = document.createElement('style');
  styleEl.id = 'qa-var-overrides';
  document.head.appendChild(styleEl);
  applyOverrides();
});
onBeforeUnmount(() => { if (styleEl) styleEl.remove(); });
watch([active, vars], applyOverrides, { deep: true });
</script>

<template>
  <div class="qa-board" style="padding-bottom:48px">
    <!-- Barre de contrôle sticky -->
    <div style="position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid #e5e5e5;padding:16px 24px;display:flex;flex-wrap:wrap;align-items:center;gap:20px">
      <div style="font:600 15px system-ui">QA Templates — {{ entries.length }}</div>

      <label style="display:flex;align-items:center;gap:8px;font:13px system-ui;cursor:pointer">
        <input type="checkbox" v-model="active" />
        Tester les variables de couleur
      </label>

      <div
        v-for="(label, key) in labels"
        :key="key"
        style="display:flex;align-items:center;gap:6px;font:12px system-ui"
        :style="{ opacity: active ? 1 : 0.4 }"
      >
        <input
          type="color"
          v-model="vars[key]"
          :disabled="!active"
          style="width:28px;height:28px;border:none;background:none;cursor:pointer;padding:0"
        />
        <span>{{ label }}</span>
      </div>

      <button
        @click="active = false"
        style="font:12px system-ui;padding:6px 12px;border:1px solid #ccc;border-radius:6px;background:#fafafa;cursor:pointer"
      >
        Reset
      </button>
    </div>

    <p style="font:13px system-ui;color:#666;margin:16px 24px;max-width:700px">
      Active le test : un template qui <strong>réagit</strong> aux curseurs lit bien les variables.
      Celui qui <strong>ne bouge pas</strong> a des couleurs hardcodées à corriger.
      Bord rouge à 390px = tout texte coupé ou déco qui dépasse est un overflow à fixer.
    </p>

    <div style="display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start;padding:0 24px">
      <div v-for="[key, cfg] in entries" :key="key" style="width:390px">
        <div style="font:13px ui-monospace,monospace;margin-bottom:8px;line-height:1.45">
          <strong style="font-size:14px">{{ cfg.name || key }}</strong><br>
          <code style="color:#888">{{ cfg.layout || cfg.id || key }}</code>
        </div>
        <div style="width:390px;height:720px;overflow-x:hidden;overflow-y:auto;border-radius:14px;outline:2px solid #e11;background:#fff">
          <CardRenderer :config="cfg" :event="mockEvent" />
        </div>
      </div>
    </div>
  </div>
</template>
