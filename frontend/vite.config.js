import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'
import fs from 'node:fs'

// Certificat mkcert (approuvé par le système / Safari). Présent en dev local.
let httpsConfig = false
try {
  httpsConfig = {
    key: fs.readFileSync('certs/localhost-key.pem'),
    cert: fs.readFileSync('certs/localhost.pem'),
  }
} catch {
  httpsConfig = false // pas de certs → dev en HTTP
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const firebaseAuthDomain =
    env.VITE_FIREBASE_AUTH_DOMAIN || 'saas-carte-de-mariage.firebaseapp.com'

  return {
    plugins: [
      vue(),
      tailwindcss(),
    ],
    server: {
      https: httpsConfig,
      // Proxy du handler d'auth Firebase pour le servir depuis localhost (même
      // origine que l'app) → contourne le blocage cross-origin de Safari.
      proxy: {
        '/__/auth': {
          target: `https://${firebaseAuthDomain}`,
          changeOrigin: true,
          secure: true,
        },
        '/__/firebase': {
          target: `https://${firebaseAuthDomain}`,
          changeOrigin: true,
          secure: true,
        },
      },
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
