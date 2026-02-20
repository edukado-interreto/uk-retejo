<template>
  <div v-if="program === undefined" class="loading">
    <n-spin size="large" />
  </div>
  <template v-else>
    <n-h1>Detala programo</n-h1>

    <program-filters
      :types="types"
      v-model:search="search"
      v-model:selected-types="selectedTypes"
      v-model:liked="filterLiked"
    />

    <n-alert v-if="filteredProgram.length === 0" title="Neniu rezulto" type="warning">
      Neniu programero estis trovita.
    </n-alert>

    <template v-else>
      <div class="buttonsList">
        <n-button
          v-for="day in days"
          :key="day"
          :disabled="programPerDay[day].length === 0"
          :type="pickedDay === day ? 'primary' : 'default'"
          @click="pickedDay = day"
        >
          {{ formattedDays[day] }}
        </n-button>
      </div>

      <program-day :program="dayProgram" />
    </template>
  </template>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { formatDateString, dayOfWeekEO } from '@/helpers/time.js';
import axios from 'axios';
import ProgramDay from '@/components/program/ProgramDay.vue';
import ProgramFilters from '@/components/program/ProgramFilters.vue';
import { useLocalStorage } from '@vueuse/core';

const program = ref(undefined);
const pickedDay = ref(null);

function fetchData() {
  axios
    .get('/program')
    .then((result) => {
      program.value = result.data;

      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based, so add 1
      const day = String(today.getDate()).padStart(2, '0');
      const formattedDate = `${year}-${month}-${day}`;

      if (days.value.includes(formattedDate)) {
        pickedDay.value = formattedDate;
      } else {
        pickedDay.value = days.value[0];
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
fetchData();

const days = computed(() => {
  const days = program.value.map((p) => p.day);
  return [...new Set(days)].sort(); // Set() removes duplicates
});
const formattedDays = computed(() => {
  const dayNames = {};
  days.value.forEach((day) => {
    dayNames[day] = `${formatDateString(day)} (${dayOfWeekEO(day)})`;
  });
  return dayNames;
});

// Filters

const search = ref('');
const selectedTypes = ref([]);
const filterLiked = ref(false);

const types = computed(() => {
  const typeList = [...new Set(program.value.map((p) => p.type))].sort((a, b) => Intl.Collator('eo').compare(a, b));
  const typeOptions = [];
  for (const type of typeList) {
    if (!!type) {
      typeOptions.push({
        label: type,
        value: type,
      });
    }
  }
  return typeOptions;
});

const storage = useLocalStorage('ukLikedTalks', []);

const filteredProgram = computed(() => {
  const searchTerm = search.value.trim().toLowerCase();
  const programWithLikes = program.value.map((t) => {
    return {
      ...t,
      liked: storage.value.includes(t.id),
    };
  });

  return programWithLikes.filter((p) => {
    const termMatch = !searchTerm
      ? true
      : p.title.toLowerCase().includes(searchTerm) || p.speakers.toLowerCase().includes(searchTerm);

    const typeMatch = selectedTypes.value.length === 0 ? true : selectedTypes.value.includes(p.type);
    const likedMatch = filterLiked.value ? p.liked : true;
    return termMatch && typeMatch && likedMatch;
  });
});

const programPerDay = computed(() => {
  const prog = {};
  for (const day of days.value) {
    prog[day] = filteredProgram.value.filter((p) => p.day === day);
  }
  return prog;
});

const dayProgram = computed(() => programPerDay.value[pickedDay.value]);

watch(
  // When filtering: go to first day with talks
  () => search.value + selectedTypes.value + filterLiked.value.toString(),
  () => {
    if (dayProgram.value.length === 0) {
      const day = days.value.find((d) => programPerDay.value[d].length > 0);
      if (day) {
        pickedDay.value = day;
      }
    }
  },
);
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 20vh;
  margin-bottom: 20vh;
  transform: scale(3);
}

.buttonsList {
  text-align: center;
  margin: 2rem 0;
}

.buttonsList button {
  margin: 0.3rem;
}
</style>
