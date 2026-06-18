<script setup>
// Mock data — swap arrays with real API responses when available
const stats = [
  { value: '2 400+', label: 'couples' },
  { value: '4.9 / 5', label: 'note moyenne' },
  { value: '18', label: 'designs exclusifs' },
  { value: '98 %', label: 'satisfaction' },
];

const reviews = [
  {
    initials: 'S & M',
    names: 'Sophie & Mathieu',
    stars: 5,
    text: 'Tellement plus élégant qu\'un carton papier. Tous nos invités ont adoré.',
    template: 'Riviera Blanche',
  },
  {
    initials: 'I & T',
    names: 'Inès & Thomas',
    stars: 5,
    text: 'Mise en place en 20 minutes. Les RSVP se sont remplis tout seuls.',
    template: 'Velvet Noir',
  },
  {
    initials: 'L & P',
    names: 'Lucie & Paul',
    stars: 5,
    text: 'Gestion des tables ultra simple. On recommande à 100 %.',
    template: 'Céleste',
  },
];
</script>

<template>
  <section class="py-20 bg-[#FEFCF8] overflow-hidden">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- Stats strip -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16 pb-16 border-b border-primary-100">
        <div v-for="stat in stats" :key="stat.label" class="text-center">
          <p class="font-serif italic text-3xl text-neutral-900 mb-1">{{ stat.value }}</p>
          <p class="text-[10px] font-bold uppercase tracking-[0.3em] text-neutral-400">{{ stat.label }}</p>
        </div>
      </div>

      <!-- Header -->
      <div class="text-center mb-12">
        <div class="flex items-center justify-center gap-0.5 mb-3" aria-label="Note 4.9 sur 5">
          <span v-for="i in 5" :key="i" class="text-primary-400 text-xl" aria-hidden="true">★</span>
          <span class="ml-3 text-sm font-light text-neutral-500">4.9 · 247 avis vérifiés</span>
        </div>
        <h2 class="text-2xl font-serif italic text-neutral-900">Ce que disent les mariés</h2>
      </div>

      <!-- Reviews -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <article v-for="review in reviews" :key="review.names"
                 class="bg-white rounded-2xl p-6 shadow-sm ring-1 ring-primary-100 flex flex-col gap-4">
          <div class="flex gap-0.5" :aria-label="`${review.stars} étoiles`">
            <span v-for="i in review.stars" :key="i" class="text-primary-400 text-sm" aria-hidden="true">★</span>
          </div>
          <p class="text-neutral-600 text-sm font-light leading-relaxed flex-grow italic">
            "{{ review.text }}"
          </p>
          <div class="flex items-center gap-3 pt-3 border-t border-primary-50">
            <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center shrink-0"
                 aria-hidden="true">
              <span class="text-[9px] font-bold text-primary-600">{{ review.initials }}</span>
            </div>
            <div>
              <p class="text-[11px] font-bold text-neutral-800">{{ review.names }}</p>
              <p class="text-[9px] text-neutral-400 uppercase tracking-widest">{{ review.template }}</p>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
