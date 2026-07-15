<template>
  <template v-if="error !== undefined">
    <congress-header />
    <n-alert :title="errorTitle" type="error">
      {{ error }}
    </n-alert>
  </template>
  <div v-else-if="data === undefined" class="loading">
    <n-spin size="large" />
  </div>
  <template v-else>
    <congress-header />
    <n-h2>Mendilo por {{ name }} (kongresnumero {{ data.KN }})</n-h2>
    <main-form :default-data="data" edit />
  </template>
</template>

<script setup>
import { ref, computed } from 'vue';
import CongressHeader from '@/components/layout/CongressHeader.vue';
import MainForm from '@/components/MainForm.vue';
import axios from 'axios';
import { useMessage } from 'naive-ui';
import { useRoute } from 'vue-router';

const data = ref(undefined);
const errorTitle = ref(undefined);
const error = ref(undefined);

const message = useMessage();
const route = useRoute();

const uniqueId = route.params.id;
if (uniqueId === undefined) {
  errorTitle.value = 'Mankanta identigilo';
  error.value = 'Se vi volas mendi servojn, bonvolu uzi la ligilon, kiu estis sendita al vi per retpoŝto.';
} else {
  fetchData();
}

const name = computed(() => `${data.value.persona_nomo} ${data.value.familia_nomo}`.trim());

function fetchData() {
  axios
    .post('/getRegistration', { id: uniqueId })
    .then((result) => {
      if (result.data.success) {
        data.value = result.data.registration;
        data.value.akcepto_reguloj = true;
        data.value.kompreno_pago = true;
      } else {
        error.value = result.data.error;
        errorTitle.value = result.data.errorTitle;
      }
    })
    .catch((error) => {
      message.error(error, {
        keepAliveOnHover: true,
      });
    });
}
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 10vh;
  margin-bottom: 10vh;
  transform: scale(3);
}
</style>
