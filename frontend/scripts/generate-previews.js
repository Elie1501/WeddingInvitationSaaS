/**
 * Génère les captures d'écran webp des templates pour la galerie landing.
 *
 * Prérequis :
 *   npm install -D playwright
 *   (ou : npx playwright install chromium)
 *
 * Usage :
 *   node scripts/generate-previews.js
 *
 * Le serveur de dev doit tourner sur http://localhost:5173 (ou ajuster BASE_URL).
 * Les images sont sauvegardées dans public/previews/{slug}.webp (600×800 px).
 */

import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const BASE_URL   = process.env.BASE_URL ?? 'http://localhost:5173';
const OUT_DIR    = resolve(__dirname, '../public/previews');
const VIEWPORT_W = 390;   // largeur mobile (iPhone 14)
const VIEWPORT_H = 844;   // hauteur de capture
const CLIP_W     = 390;
const CLIP_H     = 520;   // portion hero visible (ratio ≈ 3:4)
const DELAY_MS   = 1800;  // temps pour que les fonts/images se chargent

const SLUGS = [
  'riviera-blanche',
  'velvet-noir',
  'gatsby',
  'celestial',
  'wabi-sabi',
  'noir-eternel',
  'japonais',
  'riviera',
  'couture',
  'cinema',
  'editorial',
  'jardin-celeste',
  'empire-abstrait',
  'ora',
];

mkdirSync(OUT_DIR, { recursive: true });

const browser = await chromium.launch();

for (const slug of SLUGS) {
  const page = await browser.newPage();
  await page.setViewportSize({ width: VIEWPORT_W, height: VIEWPORT_H });

  const url = `${BASE_URL}/demo/${slug}`;
  console.log(`→ ${slug}`);

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(DELAY_MS);

  const outPath = resolve(OUT_DIR, `${slug}.webp`);
  await page.screenshot({
    path: outPath,
    type: 'webp',
    quality: 88,
    clip: { x: 0, y: 0, width: CLIP_W, height: CLIP_H },
  });

  await page.close();
  console.log(`   ✓ saved ${outPath}`);
}

await browser.close();
console.log('\nDone. All previews saved to public/previews/');
