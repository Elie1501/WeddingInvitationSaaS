import { createRouter, createWebHistory } from 'vue-router';
import LandingView from '../views/LandingView.vue';
import LoginView from '../views/LoginView.vue';
import MagicWizard from '../components/MagicWizard.vue';

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior: () => ({ top: 0 }),
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
            path: '/onboarding',
            name: 'onboarding',
            component: MagicWizard,
            meta: { requiresAuth: true }
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
            component: MagicWizard,
            meta: { requiresAuth: true }
        },
        {
          path: '/templates',
          name: 'templates',
          component: () => import('../views/TemplateGalleryView.vue'),
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
          path: '/admin/users',
          name: 'admin-users',
          component: () => import('../views/AdminUsersView.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
          path: '/admin/stats',
          name: 'admin-stats',
          component: () => import('../views/AdminStatsView.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/cards/:slug',
            name: 'public-card',
            component: () => import('../views/PublicCardView.vue')
        },
        {
            path: '/i/:slug',
            name: 'public-card-short',
            component: () => import('../views/PublicCardView.vue')
        },
        {
            path: '/demo/:slug',
            name: 'demo-card',
            component: () => import('../views/DemoCardView.vue')
            // Aucune meta requiresAuth — accessible sans connexion
        }
    ]
});

// Garde de navigation pour protéger les routes
router.beforeEach(async (to, from) => {
    const token = localStorage.getItem('token');
    
    if (to.meta.requiresAuth && !token) {
        return '/login';
    }

    // Protection admin
    if (to.meta.requiresAdmin) {
        // On récupère l'info user via le store si nécessaire
        // Note: Dans une vraie app, on vérifierait le décodage du JWT ou l'état du store
        const userStr = localStorage.getItem('user');
        if (userStr) {
            const user = JSON.parse(userStr);
            if (!user.is_admin) return '/dashboard';
        } else {
            return '/login';
        }
    }
});

export default router;
