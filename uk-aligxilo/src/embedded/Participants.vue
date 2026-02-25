<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="eo" :date-locale="dateEo">
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
import { NDialogProvider, NConfigProvider, NMessageProvider } from 'naive-ui';
import { eo, dateEo } from 'naive-ui';
import RegisteredParticipants from '@/pages/RegisteredParticipants.vue';

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
