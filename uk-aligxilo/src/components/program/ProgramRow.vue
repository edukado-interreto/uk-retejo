<template>
  <div class="program-row" :style="{ height: height + 'px', width: totalLength + 'px' }">
    <div class="room" :title="room" :style="{ width: roomWidth - 1 + 'px' }">
      <div>
        <div class="name">{{ room }}</div>
        <div class="code" v-if="roomCode" v-html="roomCode" />
      </div>
    </div>
    <div class="talks">
      <program-element
        v-for="(talk, index) in talks"
        :key="index"
        :talk="talk"
        :day-start="start"
        :hour-width="width"
        :height="height"
      />
    </div>
  </div>
</template>

<script setup>
import ProgramElement from './ProgramElement.vue';
import { computed } from 'vue';

const props = defineProps(['talks', 'room', 'roomCode', 'start', 'end', 'height', 'width', 'roomWidth', 'totalLength']);

const cols = computed(() => {
  return (props.end.getTime() - props.start.getTime()) / 3600_000;
});

const totalLength = computed(() => props.roomWidth + cols.value * props.width + 1);
</script>

<style scoped lang="scss">
.program-row {
  border: 1px solid #e6e6e6;
  border-left: none;
  border-bottom-width: 0;
  position: relative;
  display: flex;

  &:last-child {
    border-bottom-width: 1px;
  }
}

.room {
  box-sizing: border-box;
  border-left: 1px solid #e6e6e6;
  color: #444;
  padding-left: 4px;
  overflow: hidden;
  position: sticky;
  left: 0;
  background: linear-gradient(90deg, rgba(255, 255, 255, 1) 94%, rgba(255, 255, 255, 0) 100%);

  display: flex;
  align-items: center;
  z-index: 120;

  .name {
    font-weight: bold;
  }

  .code {
    font-size: 0.9em;
    hyphens: auto;
  }
}

.talks {
  position: relative;
  z-index: 110;
  padding-left: 1px;
}
</style>
