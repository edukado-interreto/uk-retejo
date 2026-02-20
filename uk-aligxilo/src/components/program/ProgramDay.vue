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
  'Hodler',
  'Höger',
  'Corsetti',
  'Gacond',
  'Podhradská',
  'Seemannová',
  'Urbanova',
  'Urbanová',
  'Kilian',
  'Schulhof ',
  'Čejka',
  'Ginz',
  'Lapenna',
  'Korto Cink',
  'korto Cink',
  'Aliloke',
  'aliloke',
];

const roomNumbers = {
  Zamenhof: 'H1 Cosmo&shy;politan – Zoner Boby Hall',
  Hodler: 'H1 Cosmo&shy;politan – London Hall',
  Höger: 'H1 Cosmo&shy;politan – Berlin Hall',
  Corsetti: 'Q01',
  Gacond: 'Q02',
  Podhradská: 'Q03',
  Seemannová: 'Q14',
  Kilian: 'Q25',
  Schulhof: 'Q28',
  Urbanová: 'Q15',
  Čejka: 'Q38',
  Ginz: 'X02',
  Lapenna: 'Konstruaĵo X',
  'Korto Cink': 'Konstruaĵo Q',
  'korto Cink': 'Konstruaĵo Q',
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
