<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="eo" :date-locale="dateEo">
    <n-global-style />
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
import { ref, useTemplateRef } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { NDialogProvider, NConfigProvider, NMessageProvider, NGlobalStyle } from 'naive-ui';
import { eo, dateEo } from 'naive-ui';

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

const themeOverrides = {
  common: {
    primaryColor: '#3366FF',
    fontFamily: 'Poppins, sans-serif',
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
  margin: 2em 0;
  border: 1px solid #ddd;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  background-color: #fff;

  @media only screen and (max-width: 1024px) {
    border-radius: 12px;
  }

  @media only screen and (max-width: 600px) {
    border-radius: 6px;
  }

  & .n-card-header {
    font-family: Unbounded, sans-serif;

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

  & + & {
    margin-top: 2.5rem;
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
