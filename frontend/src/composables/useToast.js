import { reactive } from 'vue';

// File d'attente partagée des notifications (singleton hors composant).
const state = reactive({
  toasts: [],
});

let nextId = 0;

const TITLES = {
  error: 'Erreur',
  success: 'Succès',
  info: 'Information',
  warning: 'Attention',
};

const DEFAULT_DURATION = {
  error: 6000,
  warning: 6000,
  success: 2500,
  info: 4000,
};

/**
 * Affiche une notification.
 * @param {string} message  Texte principal.
 * @param {object} [opts]
 * @param {'error'|'success'|'info'|'warning'} [opts.type]
 * @param {string} [opts.title]      Titre court (défaut selon le type).
 * @param {number} [opts.duration]   Durée en ms (0 = persistant jusqu'à fermeture).
 */
function showToast(message, opts = {}) {
  const type = opts.type || 'info';
  const id = ++nextId;
  const duration = opts.duration ?? DEFAULT_DURATION[type] ?? 4000;

  const toast = {
    id,
    message: String(message ?? ''),
    type,
    title: opts.title ?? TITLES[type],
  };

  state.toasts.push(toast);

  if (duration > 0) {
    setTimeout(() => dismissToast(id), duration);
  }
  return id;
}

function dismissToast(id) {
  const i = state.toasts.findIndex(t => t.id === id);
  if (i !== -1) state.toasts.splice(i, 1);
}

/**
 * Extrait un message lisible d'une erreur Axios / Error / string.
 */
function messageFromError(err, fallback = 'Une erreur est survenue. Veuillez réessayer.') {
  if (!err) return fallback;
  if (typeof err === 'string') return err;
  const detail = err.response?.data?.detail;
  if (typeof detail === 'string' && detail.trim()) return detail;
  // FastAPI renvoie parfois un tableau de validation
  if (Array.isArray(detail) && detail.length) {
    return detail.map(d => d.msg || d).join(' · ');
  }
  if (err.message && err.message !== 'Network Error') return err.message;
  return fallback;
}

export function useToast() {
  return {
    toasts: state.toasts,
    showToast,
    dismissToast,
    notifyError: (err, opts = {}) =>
      showToast(messageFromError(err, opts.fallback), { ...opts, type: 'error' }),
    notifySuccess: (msg, opts = {}) => showToast(msg, { ...opts, type: 'success' }),
    notifyInfo: (msg, opts = {}) => showToast(msg, { ...opts, type: 'info' }),
    notifyWarning: (msg, opts = {}) => showToast(msg, { ...opts, type: 'warning' }),
    messageFromError,
  };
}
