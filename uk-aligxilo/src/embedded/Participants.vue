<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="eo" :date-locale="dateEo">
    <n-global-style />
    <n-message-provider>
      <n-dialog-provider>
        <div v-if="loading" class="loading">
          <n-spin size="large" />
        </div>
        <registered-participants v-else />
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { NDialogProvider, NConfigProvider, NMessageProvider, NGlobalStyle } from 'naive-ui';
import { eo, dateEo } from 'naive-ui';
import RegisteredParticipants from '@/pages/RegisteredParticipants.vue';

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

const loading = ref(false);

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
