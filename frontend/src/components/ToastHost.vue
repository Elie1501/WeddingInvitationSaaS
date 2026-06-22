<template>
  <Teleport to="body">
    <div class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[300] flex flex-col items-center gap-2 w-full max-w-md px-4 pointer-events-none">
      <TransitionGroup name="toast">
        <div
          v-for="t in toasts"
          :key="t.id"
          :class="[
            'pointer-events-auto w-full rounded-2xl shadow-2xl shadow-black/20 border px-4 py-3 flex items-start gap-3',
            variant(t.type).box,
          ]"
          role="alert"
          aria-live="assertive"
        >
          <!-- Icône -->
          <div :class="['shrink-0 mt-0.5', variant(t.type).icon]">
            <!-- error -->
            <svg v-if="t.type === 'error'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <circle cx="12" cy="12" r="9" /><path stroke-linecap="round" d="M12 7v6M12 16.5h.01" />
            </svg>
            <!-- success -->
            <svg v-else-if="t.type === 'success'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <circle cx="12" cy="12" r="9" /><path stroke-linecap="round" stroke-linejoin="round" d="M8 12.5l2.5 2.5L16 9" />
            </svg>
            <!-- warning -->
            <svg v-else-if="t.type === 'warning'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3l9.5 16.5H2.5L12 3z" /><path stroke-linecap="round" d="M12 10v4M12 17h.01" />
            </svg>
            <!-- info -->
            <svg v-else class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <circle cx="12" cy="12" r="9" /><path stroke-linecap="round" d="M12 11v5M12 7.5h.01" />
            </svg>
          </div>

          <!-- Texte -->
          <div class="min-w-0 flex-1">
            <p :class="['text-[10px] font-black uppercase tracking-widest', variant(t.type).title]">{{ t.title }}</p>
            <p class="text-sm text-gray-700 mt-0.5 break-words">{{ t.message }}</p>
          </div>

          <!-- Fermer -->
          <button
            class="shrink-0 text-gray-400 hover:text-gray-700 transition-colors"
            aria-label="Fermer la notification"
            @click="dismissToast(t.id)"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '../composables/useToast';

const { toasts, dismissToast } = useToast();

const VARIANTS = {
  error:   { box: 'bg-white border-red-200',   icon: 'text-red-500',    title: 'text-red-600' },
  success: { box: 'bg-white border-green-200', icon: 'text-green-500',  title: 'text-green-600' },
  warning: { box: 'bg-white border-amber-200', icon: 'text-amber-500',  title: 'text-amber-600' },
  info:    { box: 'bg-white border-gray-200',  icon: 'text-gray-500',   title: 'text-gray-500' },
};

const variant = (type) => VARIANTS[type] || VARIANTS.info;
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.96);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.96);
}
.toast-leave-active {
  position: absolute;
  width: 100%;
}
.toast-move {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
