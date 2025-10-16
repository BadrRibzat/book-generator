import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('../views/Features.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('../views/Pricing.vue'),
  },
  {
    path: '/auth/signup',
    name: 'SignUp',
    component: () => import('../views/Auth/SignUp.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/auth/signin',
    name: 'SignIn',
    component: () => import('../views/Auth/SignIn.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('../views/Books/List.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/books/create',
    name: 'CreateBook',
    component: () => import('../views/Books/Create.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/books/:id',
    name: 'BookDetails',
    component: () => import('../views/Books/Details.vue'),
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/books/:id/covers',
    name: 'SelectCover',
    component: () => import('../views/Books/SelectCover.vue'),
    meta: { requiresAuth: true },
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Check if user is authenticated (on first load)
  if (!authStore.initialized) {
    await authStore.checkAuth();
  }

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresGuest = to.matched.some((record) => record.meta.requiresGuest);

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to sign in if not authenticated
    next({ name: 'SignIn', query: { redirect: to.fullPath } });
  } else if (requiresGuest && authStore.isAuthenticated) {
    // Redirect to books if already authenticated
    next({ name: 'Books' });
  } else {
    next();
  }
});

export default router;
