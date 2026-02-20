import { createWebHistory, createRouter } from 'vue-router';
import store from './store';

const RegistrationForm = () => import('./pages/RegistrationForm.vue');
const PriceTable = () => import('./pages/PriceTable.vue');
const RegisteredParticipants = () => import('./pages/RegisteredParticipants.vue');
const EditNotReady = () => import('./pages/EditNotReady.vue');
// const EditRegistration = () => import('./pages/EditRegistration.vue');
const NotFound = () => import('./pages/NotFound.vue');
const UnuaBulteno = () => import('./pages/UnuaBulteno.vue');
// const CongressBook = () => import('./pages/CongressBook.vue');
const AdminPage = () => import('./pages/admin/AdminPage.vue');
// const UpdateConfirmationEmails = () => import('./pages/admin/UpdateConfirmationEmails.vue');
const ClearCache = () => import('./pages/admin/ClearCache.vue');
// const CardPayment = () => import('./pages/CardPayment.vue');
// const ProgramPage = () => import('./pages/ProgramPage.vue');

const titleSuffix = 'UK 2026';

const routes = [
  {
    path: '/',
    name: 'registrationForm',
    component: RegistrationForm,
    meta: { title: 'Aliĝilo' },
  },
  {
    path: '/kotiztabelo',
    name: 'pricetable',
    component: PriceTable,
    meta: { title: 'Kotiztabelo' },
  },
  {
    path: '/aligxintoj',
    name: 'registeredParticipants',
    component: RegisteredParticipants,
    meta: { title: 'Listo de aliĝintoj' },
  },
  {
    path: '/mendilo/:id',
    name: 'editRegistration',
    component: EditNotReady,
    meta: { title: 'Mendilo' },
  },
  {
    path: '/unuabulteno',
    name: 'unuaBulteno',
    component: UnuaBulteno,
    meta: { title: 'Unua Bulteno' },
  },
  // {
  //   path: "/kongresalibro",
  //   name: "congressBook",
  //   component: CongressBook,
  // },
  // {
  //   path: '/programo',
  //   name: 'program',
  //   component: ProgramPage,
  //   meta: { title: 'Programo' },
  // },
  // {
  //   path: '/kartopago/:id',
  //   name: 'cardPayment',
  //   component: CardPayment,
  //   meta: { title: 'Pago per karto' },
  // },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
    meta: { title: 'Administrejo' },
  },
  // {
  //   path: '/admin/konfirmoj',
  //   name: 'updateConfirmationEmails',
  //   component: UpdateConfirmationEmails,
  //   beforeEnter: [checkLogin],
  //   meta: { title: 'Administrejo' },
  // },
  {
    path: '/admin/cache',
    name: 'clearCache',
    component: ClearCache,
    beforeEnter: [checkLogin],
    meta: { title: 'Administrejo' },
  },
  {
    path: '/:catchAll(.*)',
    component: NotFound,
    meta: { title: 'Ne trovita' },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

function checkLogin(to) {
  if (store.getters.isLoggedIn) {
    return true;
  }
  return { name: 'admin' };
}

router.beforeEach((to, from, next) => {
  if (to.meta.title === undefined) {
    document.title = titleSuffix;
  } else {
    document.title = to.meta.title + ' – ' + titleSuffix;
  }
  next();
});

export default router;
