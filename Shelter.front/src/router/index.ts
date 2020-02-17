import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/browse',
    name: 'browse',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Browse.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/add/step1',
    name: 'addElementStep1',
    component: () => import('../views/AddElement.vue')
  },
  {
    path: '/add/step2',
    name: 'addElementStep2',
    component: () => import('../views/AddElement.vue')
  },
  {
    path: '/add',
    redirect: '/add/step1'
  },
  {
    path: '/browse/:elementId',
    name: 'viewElement',
    component: () => import('../views/ViewElement.vue')
  },
  {
    path: '/edit/:elementId',
    name: 'editElement',
    component: () => import('../views/EditElement.vue')
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
