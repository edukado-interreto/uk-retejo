<template>
  <div class="hours-background" :style="{ 'margin-left': props.roomPadding + 'px' }">
    <div class="hours-row" :style="{ height: titleHeight + 'px' }">
      <div
        class="hour"
        v-for="(hour, index) in hours"
        :key="hour"
        :style="{
          left: index * cellWidth + 'px',
        }"
      >
        <span :class="{ secondary: !hour.endsWith('00') }">{{ hour }}</span>
      </div>
    </div>
    <div class="hours-grid">
      <div
        class="hour-column"
        v-for="(hour, index) in hours"
        :key="hour"
        :style="{
          left: index * cellWidth + 'px',
          height: totalHeight + 'px',
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { formatTime } from '@/helpers/time.js';
import { computed } from 'vue';

const props = defineProps(['start', 'end', 'step', 'rows', 'width', 'height', 'roomPadding', 'titleHeight']);

function incrementDate(dateObj) {
  return new Date(dateObj.getTime() + props.step * 60000);
}

const hours = computed(() => {
  const hours = [];
  let currentHour = props.start;

  while (currentHour.getTime() <= props.end.getTime()) {
    hours.push(formatTime(currentHour));
    currentHour = incrementDate(currentHour);
  }

  return hours;
});

const cellWidth = computed(() => (props.width * props.step) / 60);
const totalHeight = computed(() => props.rows * props.height + 2);
</script>

<style scoped lang="scss">
.hours-background {
  position: relative;
}

.hours-row {
  color: #282828;
}

.hour {
  position: absolute;

  span {
    position: relative;
    left: -50%;

    &.secondary {
      color: #9b9b9b;
    }
  }
}

.hours-grid {
  border-top: 1px solid #e6e6e6;
  position: relative;
}

.hour-column {
  position: absolute;
  top: 0;
  border-left: 1px solid #e6e6e6;
}
</style>
