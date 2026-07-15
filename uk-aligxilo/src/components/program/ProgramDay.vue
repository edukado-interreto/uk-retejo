<template>
  <n-alert v-if="rooms.length === 0" title="Neniu rezulto" type="warning">
    Neniu programero tiun tagon por la elektitaj serĉparametroj.
  </n-alert>
  <div v-else class="program-scroll" :style="{ height: rows * (CELL_HEIGHT + 4) + HOURS_ROW_HEIGHT + 10 + 'px' }">
    <div class="talks-list" :style="{ top: HOURS_ROW_HEIGHT + 'px' }">
      <program-row
        v-for="(talks, room) in programByRoom"
        :key="room"
        :start="earliest"
        :end="latest"
        :room="room"
        :talks="talks"
        :height="CELL_HEIGHT"
        :room-width="ROOM_TITLE_WIDTH"
        :width="CELL_WIDTH"
        :room-code="room in roomNumbers ? roomNumbers[room] : ''"
      />
    </div>
    <program-hours
      :start="earliest"
      :end="latest"
      :step="STEP"
      :rows="rows"
      :height="CELL_HEIGHT"
      :width="CELL_WIDTH"
      :room-padding="ROOM_TITLE_WIDTH"
      :title-height="HOURS_ROW_HEIGHT"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import ProgramHours from './ProgramHours.vue';
import ProgramRow from './ProgramRow.vue';

const props = defineProps(['program']);

const CELL_WIDTH = 170; // For 1 hour
const CELL_HEIGHT = 96;
const ROOM_TITLE_WIDTH = 116;
const HOURS_ROW_HEIGHT = 30;
const STEP = 30; // minutes

// ROOMS

const placesSort = [
  'Zamenhof',
  'Moerbeek',
  'Dobrzyński',
  'Dobrzyński /Dobĵinjski/',
  'Steiner /Ŝtajner/',
  'Steiner',
  'Franquesa Solé',
  'Fried /Fri:d/',
  'Fried',
  'Hodler',
  'Lapenna',
  'Metzger /Mecger/',
  'Metzger',
  'Haas /Ha:z/',
  'Haas',
  'Jonas',
  'Halbedl',
  'Schick /Ŝik/',
  'Schick',
  'Aliloke',
  'aliloke',
];

const roomNumbers = {
  Zamenhof: 'Stefaniensaal',
  Moerbeek: 'Kammermusiksaal',
  Dobrzyński: 'Blauer Salon',
  'Dobrzyński /Dobĵinjski/': 'Blauer Salon',
  'Steiner /Ŝtajner/': 'Saal Steiermark',
  'Franquesa Solé': 'K1+K2',
  'Fried /Fri:d/': 'K3',
  Fried: 'K3',
  Hodler: 'K4+K5',
  Lapenna: 'K6-K7',
  'Metzger /Mecger/': 'Meeting x',
  Metzger: 'Meeting x',
  'Haas /Ha:z/': 'K0',
  Haas: 'K0',
  Jonas: 'Teretaĝe',
};

const rooms = computed(() => {
  const places = props.program.map((p) => p.place);
  return [...new Set(places)].sort((a1, a2) => {
    // Set() removes duplicates
    if (placesSort.includes(a1) && placesSort.includes(a2)) {
      return placesSort.indexOf(a1) - placesSort.indexOf(a2);
    }
    if (placesSort.includes(a1)) {
      return -1;
    }
    if (placesSort.includes(a2)) {
      return 1;
    }
    return a1.localeCompare(a2);
  });
});

const programByRoom = computed(() => {
  const prog = {};
  for (const room of rooms.value) {
    prog[room] = programWithTime.value
      .filter((p) => p.place === room)
      .sort((p1, p2) => p2.start.getTime() - p1.start.getTime);
  }
  return prog;
});

const rows = computed(() => rooms.value.length);

// TIME

function roundMilliseconds(milliseconds, ceil = false) {
  const step = 1000 * 60 * STEP;
  const dividedSeconds = milliseconds / step;
  const roundedSeconds = ceil ? Math.ceil(dividedSeconds) : Math.floor(dividedSeconds);
  return roundedSeconds * step;
}

const earliest = computed(() => {
  const dates = programWithTime.value.map((p) => p.start);
  return new Date(Math.min(...dates.map((p) => roundMilliseconds(p.getTime()))));
});
const latest = computed(() => {
  const dates = programWithTime.value.map((p) => p.end);
  return new Date(Math.max(...dates.map((p) => roundMilliseconds(p.getTime(), true))));
});

const programWithTime = computed(() => {
  return props.program.map((p) => {
    return {
      ...p,
      start: new Date(`${p.day} ${p.start}`),
      end: new Date(`${p.day} ${p.end}`),
    };
  });
});

function scrollToHour(hour) {
  const scrollContainer = document.querySelector('.program-scroll');
  if (scrollContainer) {
    const scrollPosition = (hour - earliest.value.getHours()) * CELL_WIDTH;
    scrollContainer.scroll({
      left: scrollPosition,
      behavior: 'smooth',
    });
  }
}

defineExpose({
  scrollToHour,
});
</script>

<style lang="scss">
.program-scroll {
  overflow-x: scroll;
  overflow-y: hidden;
  position: relative;
  box-sizing: border-box;

  .talks-list {
    position: absolute;
    z-index: 100;
  }

  * {
    box-sizing: border-box;
  }
}
</style>
