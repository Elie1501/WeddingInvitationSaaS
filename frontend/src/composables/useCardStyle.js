import { computed, watch } from 'vue'
import { getContrastColor } from '../service/colorUtils'

const loadedFonts = new Set()

const FONT_URLS = {
  'Playfair Display': 'family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,300;1,400',
  'Cormorant Garamond': 'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400',
  'Jost': 'family=Jost:wght@300;400;600;700',
  'Dancing Script': 'family=Dancing+Script:wght@400;600;700',
}

function loadGoogleFont(fontName) {
  if (!fontName || loadedFonts.has(fontName)) return
  const query = FONT_URLS[fontName] || `family=${fontName.replace(/ /g, '+')}:ital,wght@0,300;0,400;0,700;1,300;1,400`
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = `https://fonts.googleapis.com/css2?${query}&display=swap`
  document.head.appendChild(link)
  loadedFonts.add(fontName)
}

const SIZE_PRESETS = {
  small: {
    '--size-names':     'clamp(2rem, 6vw, 3.5rem)',
    '--size-headings':  '1.75rem',
    '--size-body':      '0.85rem',
    '--size-label':     '0.6rem',
    '--size-countdown': '2.5rem',
  },
  large: {
    '--size-names':     'clamp(4.5rem, 15vw, 9rem)',
    '--size-headings':  '3.5rem',
    '--size-body':      '1.15rem',
    '--size-label':     '0.85rem',
    '--size-countdown': '5rem',
  },
}

export function useCardStyle(configRef) {
  const cssVars = computed(() => {
    const t = configRef.value?.theme || {}
    const bg       = t.background || '#F9F7F2'
    const autoText = getContrastColor(bg)
    const text     = (!t.text || t.text === '#1A1A1A') ? autoText : t.text
    const accent   = t.accent     || '#C5A059'
    const names    = t.namesColor || accent
    const headings = t.sectionTitleColor || text
    const font     = t.fontFamily || 'Playfair Display'

    const vars = {
      '--card-bg':         bg,
      '--card-text':       text,
      '--card-accent':     accent,
      '--card-names':      names,
      '--card-headings':   headings,
      '--card-font':       font,
      '--accent':          accent,
      '--accent-color':    accent,
      '--names-color':     names,
      '--title-color':     headings,
      // Nouvelles variables nommées explicitement
      '--color-bg':        bg,
      '--color-text':      text,
      '--color-names':          names,
      '--color-countdown':      t.countdownColor || accent,
      '--color-section-title':  headings,
      fontFamily:          font,
      backgroundColor:     bg,
      color:               text,
    }

    // Taille du texte — preset Petit / Moyen / Grand
    const preset = SIZE_PRESETS[t.textScale]
    if (preset) {
      Object.assign(vars, preset)
    }

    return vars
  })

  watch(
    () => configRef.value?.theme?.fontFamily,
    (font) => { if (font) loadGoogleFont(font) },
    { immediate: true }
  )

  return { cssVars }
}
