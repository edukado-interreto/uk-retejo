<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="eo" :date-locale="dateEo">
    <n-message-provider>
      <n-dialog-provider>
        <div v-if="loading" class="loading">
          <n-spin size="large" />
        </div>
        <n-alert v-if="errorMessage" :title="errorTitle" type="error">
          {{ errorMessage }}
        </n-alert>
        <main-form v-if="data !== null" :default-data="data" edit />
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { NDialogProvider, NConfigProvider, NMessageProvider } from 'naive-ui';
import { eo, dateEo } from 'naive-ui';

import MainForm from '@/components/MainForm.vue';

const loading = ref(true);

const uniqueId = ref(null);
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

const themeOverrides = {
  Layout: {
    color: '#FFFFFF00',
    textColor: 'rgba(0, 0, 0, 1)',
  },
  Common: {
    primaryColor: '#3366FF',
  },
  Checkbox: {
    border: '1px solid #909090',
  },
  Radio: {
    boxShadow: 'inset 0 0 0 1px #909090',
  },
};
</script>

<style lang="scss">
.n-card.custom-card {
  margin-top: 1.6rem;
  background: #e9f3fc;
  border-color: #99ccff;

  & .n-card-header {
    @media only screen and (max-width: 1024px) {
      padding: 0.7rem 0 0.7rem 0.7rem;
    }

    @media only screen and (max-width: 600px) {
      padding: 0.5rem 0 0.5rem 0.5rem;
      font-size: 1rem;
    }
  }

  & .n-card__content {
    @media only screen and (max-width: 1024px) {
      padding: 0 0.7rem 0.7rem 0.7rem;
    }

    @media only screen and (max-width: 600px) {
      padding: 0 0.5rem 0.5rem 0.5rem;
    }
  }

  &.margin-bottom {
    margin-top: 0.2rem;
    margin-bottom: 1.9rem;
  }
}
</style>

<style scoped>
.loading {
  text-align: center;
  margin-top: 45vh;
  transform: scale(4);
}
</style>
