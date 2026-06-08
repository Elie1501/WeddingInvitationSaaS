import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Intercepteur pour gérer le refresh du token en cas d'erreur 401
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const auth = useAuthStore();
            await auth.refreshAccessToken();
            if (auth.token) {
                originalRequest.headers.Authorization = `Bearer ${auth.token}`;
                return api(originalRequest);
            }
        }
        return Promise.reject(error);
    }
);

export default api;