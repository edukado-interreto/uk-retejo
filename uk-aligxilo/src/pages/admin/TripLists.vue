<template>
  <admin-breadcrumbs title="Ekskursoj" />
  <n-form @submit.prevent="submit">
    <n-select v-model:value="trip" :options="tripsByDay" />
    <div style="margin-top: 12px">
      <n-button :disabled="!trip" type="primary" size="large" @click="submit" :loading="loading">Elŝuti</n-button>
    </div>
  </n-form>
</template>

<script setup>
import { ref, computed } from 'vue';
import AdminBreadcrumbs from '@/components/admin/AdminBreadcrumbs.vue';
import axios from 'axios';

import { useStore } from 'vuex';

const store = useStore();
const key = store.getters.key;

const trips = store.getters.formOptions.trips;

const trip = ref(null);
const loading = ref(false);

const tripsByDay = computed(() => {
  const tripsByDayMap = {};
  trips.forEach((trip) => {
    trip.sessions.forEach((session) => {
      if (!tripsByDayMap[session.date]) {
        tripsByDayMap[session.date] = {
          type: 'group',
          label: session.date,
          key: session.date,
          children: [],
        };
      }
      tripsByDayMap[session.date].children.push({
        label: `${trip.id}. ${trip.name} (${session.name})`,
        value: session.id,
      });
    });
  });
  return Object.values(tripsByDayMap).sort((a, b) => new Date(a.key) - new Date(b.key));
});

function submit() {
  loading.value = true;
  axios
    .post('/admin/triplist', { key, trip: trip.value }, { responseType: 'blob' })
    .then((response) => {
      const blob = new Blob([response.data], { type: 'text/html' });
      const url = URL.createObjectURL(blob);

      window.open(url, '_blank');
    })
    .finally(() => {
      loading.value = false;
    });
}
</script>
