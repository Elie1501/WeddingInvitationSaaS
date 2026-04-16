<script setup>
import { computed } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  mode: { type: String, default: 'full' }
});

const theme = computed(() => props.config.theme || { accent: '#000000', text: '#1a1a1a', background: '#ffffff' });
const content = computed(() => props.config.content || {});

const displayNames = computed(() => content.value.names || `${props.event.groom_name || 'Élie'} & ${props.event.bride_name || 'Sarah'}`);
const displayDate = computed(() => {
  if (!props.event.date) return 'DATE À VENIR';
  return new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }).toUpperCase();
});
</script>

<template>
  <div class="es-block" :style="{ '--accent': theme.accent, '--text': theme.text, '--bg': theme.background, fontFamily: theme.fontFamily || 'Inter' }">
    
    <!-- ES HERO -->
    <div v-if="mode === 'es-hero' || mode === 'full'" class="es-hero">
      <div class="es-hero-content">
        <div class="es-monogram">ES</div>
        <h1 class="es-names">{{ displayNames }}</h1>
        <div class="es-divider"></div>
        <p class="es-date">{{ displayDate }}</p>
      </div>
      <div class="es-hero-image" :style="{ backgroundImage: `url(${content.image_url || 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200'})` }"></div>
    </div>

    <!-- ES INTRO -->
    <div v-if="mode === 'es-intro' || mode === 'full'" class="es-section es-intro">
      <p class="es-label">Invitation</p>
      <h2 class="es-title">Nous nous marions</h2>
      <p class="es-text">
        {{ content.intro_text || 'C\'est avec une immense joie que nous vous invitons à célébrer notre union. Votre présence à nos côtés rendra cette journée inoubliable.' }}
      </p>
    </div>

    <!-- ES DETAILS -->
    <div v-if="mode === 'es-details' || mode === 'full'" class="es-section es-details">
      <div class="es-detail-item">
        <p class="es-label">Quand</p>
        <p class="es-detail-value">{{ displayDate }}</p>
        <p class="es-detail-sub" v-if="event.time">{{ event.time }}</p>
      </div>
      <div class="es-detail-item">
        <p class="es-label">Où</p>
        <p class="es-detail-value">{{ event.location || 'Lieu à définir' }}</p>
      </div>
      <div class="es-actions">
        <a v-if="event.location" :href="`https://waze.com/ul?q=${encodeURIComponent(event.location)}`" class="es-btn" target="_blank">Itinéraire</a>
      </div>
    </div>

    <!-- ES FOOTER -->
    <div v-if="mode === 'es-footer' || mode === 'full'" class="es-footer">
      <div class="es-monogram-small">ES</div>
      <p>{{ content.footer_text || 'Hâte de vous retrouver' }}</p>
    </div>

  </div>
</template>

<style scoped>
.es-block {
  width: 100%;
  background-color: var(--bg);
  color: var(--text);
  text-align: center;
}

.es-hero {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  padding: 40px;
}

.es-hero-content {
  z-index: 2;
  background: rgba(255, 255, 255, 0.9);
  padding: 60px 40px;
  border: 1px solid var(--accent);
}

.es-monogram {
  font-size: 0.8rem;
  letter-spacing: 0.5em;
  font-weight: 800;
  margin-bottom: 20px;
  color: var(--accent);
}

.es-names {
  font-size: 3rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  line-height: 1;
  margin-bottom: 30px;
}

.es-divider {
  width: 40px;
  height: 4px;
  background-color: var(--accent);
  margin: 0 auto 30px;
}

.es-date {
  font-size: 0.9rem;
  letter-spacing: 0.3em;
  font-weight: 500;
}

.es-hero-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.es-section {
  padding: 100px 40px;
  max-width: 600px;
  margin: 0 auto;
}

.es-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.4em;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 20px;
}

.es-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 30px;
}

.es-text {
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.8;
}

.es-detail-item {
  margin-bottom: 40px;
}

.es-detail-value {
  font-size: 1.4rem;
  font-weight: 700;
}

.es-detail-sub {
  font-size: 0.9rem;
  opacity: 0.6;
  margin-top: 5px;
}

.es-actions {
  margin-top: 50px;
}

.es-btn {
  display: inline-block;
  padding: 15px 40px;
  background-color: var(--accent);
  color: white;
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  transition: all 0.3s ease;
}

.es-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.es-footer {
  padding: 80px 40px;
  border-top: 1px solid #eee;
  font-size: 0.8rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  opacity: 0.5;
}

.es-monogram-small {
  font-weight: 800;
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .es-names {
    font-size: 2.2rem;
  }
}
</style>
