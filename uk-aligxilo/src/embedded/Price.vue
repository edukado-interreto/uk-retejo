<template>
  <base-app>
    <div v-if="loading" class="loading">
      <n-spin size="large" />
    </div>
    <price-table v-else />
  </base-app>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import BaseApp from './BaseApp.vue';
import PriceTable from '@/pages/PriceTable.vue';

const loading = ref(true);

const store = useStore();

function loaddata() {
  store.dispatch('loaddata').then(() => {
    loading.value = false;
  });
}

loaddata();
</script>
