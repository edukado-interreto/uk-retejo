<template>
  <base-app>
    <div v-if="loading" class="loading">
      <n-spin size="large" />
    </div>
    <registered-participants v-else />
  </base-app>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import BaseApp from './BaseApp.vue';
import RegisteredParticipants from '@/pages/RegisteredParticipants.vue';

const loading = ref(false);

const store = useStore();

function loaddata() {
  store.dispatch('loaddata').then(() => {
    loading.value = false;
  });
}

loaddata();
</script>
