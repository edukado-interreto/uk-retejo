<template>
  <p style="font-size: 1.3em; margin-top: -1rem">Mi mendas la jenajn ekskursojn:</p>
  <h5>Tuttagaj ekskursoj:</h5>
  <form-trips-trip
    v-for="trip in formOptions.trips.filter((t) => t.fullDay)"
    :key="trip.id"
    v-model="modelValue"
    :trip="trip"
    :full-trips="fullTrips"
    :disabled-trips="disabledTrips"
  />
  <h5>Duontagaj ekskursoj:</h5>
  <form-trips-trip
    v-for="trip in formOptions.trips.filter((t) => !t.fullDay)"
    :key="trip.id"
    v-model="modelValue"
    :trip="trip"
    :full-trips="fullTrips"
    :disabled-trips="disabledTrips"
  />
</template>

<script setup>
import FormTripsTrip from './FormTripsTrip.vue';
import { computed } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  modelValue: Object,
  defaultTrips: Array, // Trips already picked by user before loading the form
});

const modelValue = defineModel('modelValue');

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);

const sessionsList = computed(() => {
  const sessions = [];
  formOptions.value.trips.forEach((t) => {
    t.sessions.forEach((s) => {
      sessions.push({
        ...s,
        trip: t.id,
      });
    });
  });
  return sessions;
});

const fullTrips = computed(() => {
  const fullTripsArr = [];
  sessionsList.value.forEach((trip) => {
    if (!trip.available && !props.defaultTrips.includes(trip.id)) {
      fullTripsArr.push(trip.id);
    }
  });
  return fullTripsArr;
});

const disabledTrips = computed(() => {
  const usedDates = [];
  const usedTrips = [];
  sessionsList.value.forEach((trip) => {
    if (modelValue.value.includes(trip.id)) {
      usedDates.push({
        day: trip.date,
        start: trip.start,
        end: trip.end,
      });
      usedTrips.push(trip.trip);
    }
  });

  const disabled = [];
  fullTrips.value.forEach((trip) => {
    // Full trips
    disabled.push(trip);
  });
  sessionsList.value.forEach((trip) => {
    // Trips happening at the same time
    const incompatibleDate = usedDates.find((d) => {
      return d.day === trip.date && d.start < trip.end && d.end > trip.start;
    });
    if ((usedTrips.includes(trip.trip) || incompatibleDate !== undefined) && !modelValue.value.includes(trip.id)) {
      disabled.push(trip.id);
    }
  });
  return disabled;
});
</script>

<style scoped>
h5 {
  font-size: 1.2rem;
  color: #3366ff;
  font-weight: normal;
  margin-bottom: 0;
}
</style>
