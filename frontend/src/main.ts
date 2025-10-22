import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import LoginView from './account/views/LoginView.vue';
import AdminView from './views/AdminView.vue';
import UserMenuView from './views/UserMenuView.vue';
import ScheduleView from './schedule/views/ScheduleView.vue';
import DayBoxTest from './schedule/views/DayBoxTest.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminView
    },
    {
      path: '/user',
      name: 'UserMenu',
      component: UserMenuView
    },
    {
      path: '/schedule',
      name: 'Schedule',
      component: ScheduleView
    },
    {
      path: '/daybox-test',
      name: 'DayBoxTest',
      component: DayBoxTest
    }
  ]
});

const app = createApp(App);
app.use(router);
app.mount('#app');
