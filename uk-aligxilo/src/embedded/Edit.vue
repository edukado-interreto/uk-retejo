<template>
  <base-app>
    <div v-if="loading" class="loading">
      <n-spin size="large" />
    </div>
    <n-alert v-if="errorMessage" :title="errorTitle" type="error">
      {{ errorMessage }}
    </n-alert>
    <main-form v-if="data !== null" :default-data="data" edit />
  </base-app>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import BaseApp from './BaseApp.vue';
import MainForm from '@/components/MainForm.vue';

const loading = ref(true);

const errorTitle = ref(null);
const errorMessage = ref(null);

const data = ref(null);

const fetchData = (id) => {
  loading.value = true;
  axios
    .post('/getRegistration', { id })
    .then((result) => {
      if (result.data.success) {
        data.value = result.data.registration;
        data.value.akcepto_reguloj = true;
        data.value.kompreno_pago = true;
      } else {
        errorMessage.value = result.data.error;
        errorTitle.value = result.data.errorTitle;
      }
    })
    .catch((error) => {
      errorTitle.value = `Eraro: „${error.message}”`;
      errorMessage.value = `Ne eblis preni la datumojn por la mendilo „${id}”`;
    })
    .finally(() => {
      loading.value = false;
    });
};

const match = /mendilo\/(?<id>\w+)/.exec(window.location.pathname);
if (match === null) {
  errorTitle.value = 'Mankanta identigilo';
  errorMessage.value = 'Se vi volas mendi servojn, bonvolu uzi la ligilon, kiu estis sendita al vi per retpoŝto.';
} else {
  useStore()
    .dispatch('loaddata')
    .then(() => {
      fetchData(match.groups.id);
    });
}
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 45vh;
  transform: scale(4);
}
</style>
