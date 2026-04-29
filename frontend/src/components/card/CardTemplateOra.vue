<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  subEvents: { type: Array, default: () => [] },
  mode: { type: String, default: 'full' } 
  // Modes: 'hero', 'section1', 'parallax', 'section2', 'tribute', 'gallery', 'footer'
});

const content = computed(() => props.config.content || {});
const theme = computed(() => props.config.theme || { accent: '#C5A059', text: '#1a1a1a', background: '#ffffff' });

const displayNames = computed(() => content.value.names || `${props.event.groom_name || 'Ora'} & ${props.event.bride_name || 'Samuel'}`);
const displayDate = computed(() => props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).toUpperCase() : 'DATE À VENIR');

// Animation des pétales
const petalsContainer = ref(null);
let petalInterval = null;

const createPetal = () => {
  if (!petalsContainer.value || content.value.show_petals === false) return;
  const petal = document.createElement('div');
  petal.className = 'petal';
  const size = Math.random() * 8 + 5;
  petal.style.width = size + 'px';
  petal.style.height = size * 1.5 + 'px';
  petal.style.left = Math.random() * 100 + '%';
  petal.style.top = '-20px';
  petal.style.animation = `fall ${Math.random() * 3 + 4}s linear forwards`;
  petalsContainer.value.appendChild(petal);
  setTimeout(() => petal.remove(), 7000);
};

onMounted(() => {
  if (props.mode === 'hero' || props.mode === 'full') {
    petalInterval = setInterval(createPetal, 600);
  }
});

onUnmounted(() => {
  if (petalInterval) clearInterval(petalInterval);
});
</script>

<template>
  <div class="ora-block" :style="{ '--gold': theme.accent, '--text-dark': theme.text, '--bg-light': theme.background }">
    
    <!-- BLOC HERO -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-wrapper">
        <div ref="petalsContainer" class="petals-wrapper"></div>
        <div class="hero-image" :style="{ backgroundImage: `url(${content.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'})` }">
            <div class="hero-overlay"></div>
        </div>
        <div class="container relative z-10">
            <h1 class="main-names">{{ displayNames }}</h1>
            <div class="luxury-divider">
                <span class="divider-symbol">{{ content.divider_symbol || '✧' }}</span>
            </div>
        </div>
    </div>

    <!-- BLOC SECTION 1 (MAIRIE) -->
    <div v-if="mode === 'section1' || mode === 'full'" class="container">
        <section class="event-section no-border">
            <p class="label">{{ content.s1_label || 'Union Civile' }}</p>
            <h2 class="event-title">{{ content.s1_title || 'La Mairie' }}</h2>
            <p class="details">{{ content.s1_date || displayDate }}</p>
            <p class="address" v-html="(content.s1_location || event.location || 'Lieu à définir').replace('\n', '<br>')"></p>
            <div class="btn-group">
                <a :href="`https://waze.com/ul?q=${encodeURIComponent(content.s1_location || event.location)}`" class="btn" target="_blank">Waze</a>
                <button class="btn">Calendrier</button>
            </div>
            <!-- Vin d'honneur -->
            <div v-if="content.s1_extra_title" style="margin-top: 40px;">
                <p class="label" style="font-size: 0.6rem;">{{ content.s1_extra_label || "Vin d'honneur" }}</p>
                <p class="address" style="font-size: 1.1rem;" v-html="content.s1_extra_title.replace('\n', '<br>')"></p>
                <a v-if="content.s1_extra_location" :href="`https://waze.com/ul?q=${encodeURIComponent(content.s1_extra_location)}`" class="btn" target="_blank">Waze</a>
            </div>
        </section>
    </div>

    <!-- BLOC PARALLAX -->
    <div v-if="(mode === 'parallax' || mode === 'full') && content.parallax_image_url" 
         class="parallax-section" 
         :style="{ backgroundImage: `url(${content.parallax_image_url})` }">
    </div>

    <!-- BLOC SECTION 2 (RELIGIEUX / FAMILLES) -->
    <div v-if="mode === 'section2' || mode === 'full'" class="container">
        <section class="event-section">
            <p class="label">{{ content.s2_label || 'Cérémonie Religieuse' }}</p>
            <h2 class="event-title">{{ content.s2_title || 'Houppa & Soirée' }}</h2>
            
            <div class="families-wrapper">
                <div class="family-left text-left">
                    <p class="family-title">{{ content.family_left_title || 'Famille' }}</p>
                    <p class="parents-names" v-html="content.family_left_parents?.replace('\n', '<br>') || 'Parents'"></p>
                </div>
                <div class="family-right text-right">
                    <p class="family-title">{{ content.family_right_title || 'Famille' }}</p>
                    <p class="parents-names" v-html="content.family_right_parents?.replace('\n', '<br>') || 'Parents'"></p>
                </div>
            </div>

            <p class="announcement-text">{{ content.announcement_text || 'Ont la joie de vous faire part du mariage de leurs enfants' }}</p>
            <div v-if="content.hebrew_names" class="hebrew">{{ content.hebrew_names }}</div>
            <p class="intro-text">{{ content.intro_text_s2 || 'Seront honorés de votre présence...' }}</p>
            
            <p class="details">{{ content.s2_date || displayDate }}</p>
            <p class="address" v-html="(content.s2_location || 'Lieu à définir').replace('\n', '<br>')"></p>

            <div class="btn-group">
                <a :href="`https://waze.com/ul?q=${encodeURIComponent(content.s2_location)}`" class="btn" target="_blank">Waze</a>
                <button class="btn">Calendrier</button>
            </div>
        </section>
    </div>

    <!-- BLOC HOMMAGE -->
    <div v-if="mode === 'tribute' || mode === 'full'" class="container">
        <div v-if="content.tribute_title || content.tribute_text" class="tribute-card">
            <p class="tribute-title">{{ content.tribute_title || 'Une pensée pour nos disparus' }}</p>
            <p class="tribute-text" v-html="content.tribute_text?.replace('\n', '<br>')"></p>
            <p class="tribute-blessing">{{ content.tribute_blessing }}</p>
        </div>
    </div>

    <!-- BLOC GALERIE -->
    <div v-if="mode === 'gallery' || mode === 'full'" class="container">
        <section class="photo-gallery">
            <p class="label" style="margin-bottom: 30px;">{{ content.gallery_label || 'Nos Souvenirs' }}</p>
            <div class="gallery-grid">
                <div class="gallery-item"><img :src="content.gal_img1 || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800'"></div>
                <div class="gallery-item"><img :src="content.gal_img2 || 'https://images.unsplash.com/photo-1510076857177-7470076d4098?w=400'"></div>
                <div class="gallery-item"><img :src="content.gal_img3 || 'https://images.unsplash.com/photo-1522673607200-1648832cee98?w=400'"></div>
            </div>
        </section>
    </div>

    <!-- BLOC FOOTER -->
    <div v-if="mode === 'footer' || mode === 'full'" class="ora-footer">
        {{ content.footer_text || `${event.groom_name?.[0] || 'O'} & ${event.bride_name?.[0] || 'S'} — 2026` }}
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@200;300;400;600&display=swap');

.ora-block {
    --gold: #C5A059;
    --text-dark: #1a1a1a;
    --bg-light: #ffffff;
    background-color: var(--bg-light);
    color: var(--text-dark);
    font-family: 'Montserrat', sans-serif;
    line-height: 1.5;
    text-align: center;
    width: 100%;
}

.hero-wrapper { position: relative; width: 100%; }

.petals-wrapper {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 50;
    overflow: hidden;
}

:deep(.petal) {
    position: absolute;
    background: linear-gradient(135deg, #fdfbf7 0%, var(--gold) 100%);
    border-radius: 150% 0 150% 0;
    opacity: 0.3;
}

@keyframes fall {
    to { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}

.hero-image {
    width: 100%;
    height: 45vh;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    position: relative;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, transparent 50%, var(--bg-light) 95%);
}

.parallax-section {
    width: 100%;
    height: 40vh;
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    margin: 20px 0;
}

@media (max-width: 768px) {
    .parallax-section { background-attachment: scroll; }
}

.container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 0 20px;
}

.main-names {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 300;
    font-style: italic;
    margin: -25px 0 20px;
    position: relative;
    animation: fadeInUp 1.2s ease-out;
}

.luxury-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 40px;
    width: 80%;
}

.luxury-divider::before, .luxury-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
}

.divider-symbol {
    font-family: 'Cormorant Garamond', serif;
    color: var(--gold);
    font-size: 1.5rem;
    margin: 0 15px;
}

.event-section {
    padding: 50px 0;
    border-top: 1px solid #f5f5f5;
}

.event-section.no-border { border-top: none; }

.label {
    font-size: 0.7rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 15px;
    font-weight: 600;
}

.event-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 300;
    margin-bottom: 10px;
}

.details {
    font-size: 1rem;
    font-weight: 400;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.address {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.25rem;
    color: #666;
    margin-bottom: 25px;
}

.btn-group {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
}

.btn {
    padding: 12px 20px;
    border: 1px solid var(--gold);
    color: var(--gold);
    text-decoration: none;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    min-width: 110px;
    background: none;
    transition: 0.3s;
    cursor: pointer;
}

.btn:hover { background: var(--gold); color: white; }

.families-wrapper {
    display: flex;
    justify-content: space-between;
    margin: 30px 0 20px;
}

.family-left, .family-right { width: 48%; }

.family-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 8px;
}

.parents-names {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    font-size: 1.05rem;
    line-height: 1.2;
}

.announcement-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    font-style: italic;
    color: #555;
    margin: 20px 0 30px;
}

.hebrew {
    font-size: 2.5rem;
    margin: 10px 0;
    font-family: 'Cormorant Garamond', serif;
    color: var(--gold);
}

.intro-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-style: italic;
    margin: 15px 0;
    color: #444;
}

.tribute-card {
    background-color: #fafafa;
    border-radius: 4px;
    padding: 25px 15px;
    margin: 35px auto 20px;
    border-left: 1px solid var(--gold);
    border-right: 1px solid var(--gold);
}

.tribute-title {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-weight: 600;
    margin-bottom: 10px;
}

.tribute-text {
    color: #555;
    font-size: 1rem;
    margin-bottom: 10px;
    font-family: 'Cormorant Garamond', serif;
}

.tribute-blessing {
    color: var(--gold);
    font-weight: 600;
    font-size: 0.95rem;
    font-family: 'Cormorant Garamond', serif;
}

.photo-gallery { padding: 60px 0; }
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 12px;
}
.gallery-item:first-child { grid-column: span 2; }
.gallery-item img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }

.ora-footer {
    padding: 60px 0;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: var(--gold);
    text-transform: uppercase;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
