<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="eo" :date-locale="dateEo">
    <n-message-provider>
      <n-dialog-provider>
        <div v-if="loading" class="loading">
          <n-spin size="large" />
        </div>
        <application v-else />
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { ref } from 'vue';
import Application from './components/layout/Application.vue';
import { useStore } from 'vuex';
import { NDialogProvider, NConfigProvider, NMessageProvider } from 'naive-ui';
import { eo, dateEo } from 'naive-ui';

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

const loading = ref(true);

const store = useStore();

function loaddata() {
  store.dispatch('loaddata').then(() => {
    loading.value = false;
  });
}

loaddata();
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
