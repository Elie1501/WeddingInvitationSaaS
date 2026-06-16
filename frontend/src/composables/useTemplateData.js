// composables/useTemplateData.js
// ============================================================================
// Phase 1 — Source unique de la logique partagée entre TOUS les templates.
// Remplace le copier-coller (tick countdown, isLoaded, displayNames…) répété
// ~15 fois dans le codebase.
//
// Réactivité : on accepte des GETTERS (() => props.config) plutôt que les
// objets bruts. toValue() les déréférence proprement, donc tout reste réactif
// même si la config change en live dans l'éditeur. C'est ce qui corrige le bug
// "le compte à rebours ne s'adapte pas quand on change la date".
//
// Usage dans un template :
//   const { displayNames, displayDate, displayLocation, timeLeft, isLoaded, subEvents }
//     = useTemplateData(() => props.config, () => props.event);
// ============================================================================

import { ref, computed, watch, onMounted, onBeforeUnmount, toValue } from 'vue';

export function useTemplateData(config, event) {
  // Accès réactifs et défensifs (jamais d'accès direct qui casse si undefined)
  const cfg     = computed(() => toValue(config) ?? {});
  const content = computed(() => cfg.value.content ?? {});
  const evt     = computed(() => toValue(event) ?? {});

  // ── Données d'affichage ───────────────────────────────────────────────────
  const displayNames = computed(() => {
    if (content.value.names) return content.value.names;
    const g = evt.value.groom_name ?? '';
    const b = evt.value.bride_name ?? '';
    const joined = `${g} & ${b}`.trim();
    return joined === '&' ? 'Les mariés' : joined;
  });

  const displayLocation = computed(
    () => content.value.address || evt.value.location || ''
  );

  // sub_events : vérifie d'abord à la racine du config (pattern des nouvelles
  // configs), puis dans content, puis dans l'event en dernier recours.
  const subEvents = computed(
    () => cfg.value.sub_events || content.value.sub_events || evt.value.sub_events || []
  );

  // ── Date : une seule source de vérité, parsée une fois, réactive ─────────
  // event.date = date ISO calculable. config.content.date = override éventuel.
  const targetDate = computed(() => {
    const raw = evt.value.date || content.value.date;
    if (!raw) return null;
    const d = new Date(raw);
    return Number.isNaN(d.getTime()) ? null : d;
  });

  // Texte affiché : priorité au libellé custom, sinon format FR depuis la date.
  const displayDate = computed(() => {
    if (content.value.date_display) return content.value.date_display;
    if (!targetDate.value) return '';
    return targetDate.value.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  });

  // ── Compte à rebours ──────────────────────────────────────────────────────
  const timeLeft = ref({ days: 0, hours: 0, mins: 0, secs: 0, isPast: false });

  function computeTimeLeft() {
    const target = targetDate.value;
    if (!target) {
      timeLeft.value = { days: 0, hours: 0, mins: 0, secs: 0, isPast: false };
      return;
    }
    const diff = target.getTime() - Date.now();
    if (diff <= 0) {
      timeLeft.value = { days: 0, hours: 0, mins: 0, secs: 0, isPast: true };
      return;
    }
    const totalSecs = Math.floor(diff / 1000);
    timeLeft.value = {
      days:  Math.floor(totalSecs / 86400),
      hours: Math.floor((totalSecs % 86400) / 3600),
      mins:  Math.floor((totalSecs % 3600) / 60),
      secs:  totalSecs % 60,
      isPast: false,
    };
  }

  let timer = null;
  onMounted(() => {
    computeTimeLeft();
    timer = setInterval(computeTimeLeft, 1000);
  });
  onBeforeUnmount(() => {
    if (timer) clearInterval(timer);
  });

  // Recalcul immédiat quand la date change dans l'éditeur (live).
  watch(targetDate, computeTimeLeft);

  // ── Entrée (animation de montage) ─────────────────────────────────────────
  const isLoaded = ref(false);
  onMounted(() => {
    setTimeout(() => { isLoaded.value = true; }, 100);
  });

  return {
    displayNames,
    displayDate,
    displayLocation,
    timeLeft,
    isLoaded,
    subEvents,
  };
}
