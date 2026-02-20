<template>
  <div class="trip">
    <h6>
      {{ trip.id }}. {{ trip.name }} – {{ trip.price }}&nbsp;€
      <n-button text style="font-size: 24px" v-if="trip.description" @click="showDescription(trip)">
        <n-icon color="#2050cf">
          <InformationCircleOutline />
        </n-icon>
      </n-button>
    </h6>
    <div v-if="trip.subtitle" style="margin-top: 2px">{{ trip.subtitle }}</div>
    <form-trips-sessions-checkboxes
      v-model="modelValue"
      :sessions="trip.sessions"
      :full-trips="fullTrips"
      :disabled-trips="disabledTrips"
    />
  </div>

  <n-modal v-model:show="showModal" preset="card" style="max-width: 900px" :title="descriptionTitle" size="small">
    <div v-html="descriptionText"></div>
  </n-modal>
</template>

<script setup>
import { ref } from 'vue';
import { NIcon } from 'naive-ui';
import InformationCircleOutline from '@/components/ui/icons/InformationCircleOutline.vue';
import FormTripsSessionsCheckboxes from './FormTripsSessionsCheckboxes.vue';

const props = defineProps({
  trip: Array,
  fullTrips: Array,
  disabledTrips: Array,
});

const modelValue = defineModel('modelValue');

// Modal
const showModal = ref(false);
const descriptionTitle = ref('');
const descriptionText = ref('');

function showDescription(option) {
  descriptionTitle.value = option.id + '. ' + option.name;
  descriptionText.value = option.description;
  showModal.value = true;
}
</script>

<style scoped>
div.trip {
  margin-top: 1.5rem;
}

h6 {
  font-size: 1rem;
  margin: 0;
  display: flex;
}

button {
  margin-left: 5px;
  top: 1px;
}
</style>
