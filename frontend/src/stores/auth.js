import { defineStore } from 'pinia';
import api from '../service/api';
import { auth, provider } from '../firebase';
import { signInWithPopup } from 'firebase/auth';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
    }),
    actions: {
        async loginWithGoogle() {
            try {
                const result = await signInWithPopup(auth, provider);
                const idToken = await result.user.getIdToken();

                const response = await api.post('/auth/google', {
                    id_token: idToken
                });

                this.token = response.data.access_token;
                this.refreshToken = response.data.refresh_token;
                localStorage.setItem('token', this.token);
                localStorage.setItem('refresh_token', this.refreshToken);
                await this.fetchMe();
                return { isNewUser: response.data.is_new_user || false };
            } catch (error) {
                console.error("Google Login Error:", error);
                throw error;
            }
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