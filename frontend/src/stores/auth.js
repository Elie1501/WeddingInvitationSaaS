import { defineStore } from 'pinia';
import api from '../service/api';
import { auth, provider } from '../firebase';
import { signInWithPopup, signInWithRedirect, getRedirectResult } from 'firebase/auth';

// Safari / iOS (WebKit) bloquent la communication popup cross-domaine (ITP) :
// signInWithPopup fait planter la page. On bascule sur la redirection pour ces navigateurs.
function shouldUseGoogleRedirect() {
    const ua = navigator.userAgent;
    const isIOS = /iPad|iPhone|iPod/.test(ua) ||
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const isSafari = /^((?!chrome|crios|fxios|edg|android).)*safari/i.test(ua);
    return isIOS || isSafari;
}

export const useAuthStore = defineStore('auth', {
    state: () => {
        let user = null;
        try {
            const saved = localStorage.getItem('user');
            if (saved) user = JSON.parse(saved);
        } catch {}
        return {
            user,
            token: localStorage.getItem('token') || null,
            refreshToken: localStorage.getItem('refresh_token') || null,
        };
    },
    actions: {
        // Échange l'id_token Firebase contre nos JWT et hydrate l'utilisateur.
        async _completeGoogleLogin(idToken, plan) {
            const response = await api.post('/auth/google', {
                id_token: idToken,
                plan
            });
            this.token = response.data.access_token;
            this.refreshToken = response.data.refresh_token;
            localStorage.setItem('token', this.token);
            localStorage.setItem('refresh_token', this.refreshToken);
            await this.fetchMe();
            return { isNewUser: response.data.is_new_user || false };
        },
        async loginWithGoogle(plan = 'classic') {
            // Safari / iOS : la popup plante → on redirige vers Google.
            // Le retour est finalisé par finishGoogleRedirect() au montage de la vue.
            if (shouldUseGoogleRedirect()) {
                sessionStorage.setItem('google_auth_plan', plan);
                sessionStorage.setItem('google_auth_pending', '1');
                await signInWithRedirect(auth, provider);
                return { redirecting: true };
            }
            try {
                const result = await signInWithPopup(auth, provider);
                const idToken = await result.user.getIdToken();
                return await this._completeGoogleLogin(idToken, plan);
            } catch (error) {
                console.error("Google Login Error:", error);
                throw error;
            }
        },
        // À appeler au chargement des pages login/register pour finaliser
        // une connexion Google initiée via redirection (Safari / iOS).
        async finishGoogleRedirect() {
            if (sessionStorage.getItem('google_auth_pending') !== '1') return null;
            sessionStorage.removeItem('google_auth_pending');
            const plan = sessionStorage.getItem('google_auth_plan') || 'classic';
            sessionStorage.removeItem('google_auth_plan');

            let result;
            try {
                result = await getRedirectResult(auth);
            } catch (error) {
                console.error("Google Redirect Error:", error);
                throw error;
            }
            if (!result || !result.user) return null;

            const idToken = await result.user.getIdToken();
            return await this._completeGoogleLogin(idToken, plan);
        },
        async login(email, password) {
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);

            const response = await api.post('/auth/login', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            this.token = response.data.access_token;
            this.refreshToken = response.data.refresh_token;
            localStorage.setItem('token', this.token);
            localStorage.setItem('refresh_token', this.refreshToken);
            await this.fetchMe();
        },
        async register(email, password) {
            await api.post('/auth/signup', { email, password });
            await this.login(email, password);
        },
        async fetchMe() {
            try {
                const response = await api.get('/auth/me');
                this.user = response.data;
                // Sauvegarder l'utilisateur pour le navigation guard
                localStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                this.logout();
            }
        },
        async refreshAccessToken() {
            if (!this.refreshToken) return;
            try {
                const response = await api.post('/auth/refresh-token', { refresh_token: this.refreshToken });
                this.token = response.data.access_token;
                this.refreshToken = response.data.refresh_token;
                localStorage.setItem('token', this.token);
                localStorage.setItem('refresh_token', this.refreshToken);
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    }
});