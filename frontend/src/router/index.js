import { createRouter, createWebHistory } from 'vue-router';
import LandingView from '../views/LandingView.vue';
import LoginView from '../views/LoginView.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: LandingView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../views/DashboardView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/events/create',
            name: 'create-event',
            component: () => import('../views/CreateEventView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/cards/edit/:id',
            name: 'edit-card',
            component: () => import('../views/CardEditorView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/events/:id/guests',
            name: 'event-guests',
            component: () => import('../views/GuestManagementView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/events/:id/tables',
            name: 'event-tables',
            component: () => import('../views/TableManagementView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/cards/:slug',
            name: 'public-card',
            component: () => import('../views/PublicCardView.vue')
        }
    ]
});

// Garde de navigation pour protéger les routes
router.beforeEach((to, from) => {
    const token = localStorage.getItem('token');
    
    if (to.meta.requiresAuth && !token) {
        // Rediriger vers login si on n'est pas connecté
        return '/login';
    }
});

export default router;
