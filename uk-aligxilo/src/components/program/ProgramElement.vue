<template>
  <div
    class="talk"
    :style="{ height: height - 3 + 'px', left: left + 'px', width: width + 'px' }"
    :class="bgClasses"
    :title="`${start}–${end} ${talk.title}`"
    @click="showModal = true"
  >
    <div class="liked" v-if="talk.liked" title="Ŝatata programero">♥</div>
    <div class="info">
      <span class="hour">{{ start }}–{{ end }}</span>
      <template v-if="talk.type"> • {{ talk.type }}</template>
    </div>
    <div class="title">
      {{ talk.title }}
    </div>
    <div v-if="talk.speakers" class="speakers">
      {{ talk.speakers }}
    </div>
  </div>
  <program-details :talk="talk" :show="showModal" @close="showModal = false" />
</template>

<script setup>
import { formatTime } from '@/helpers/time.js';
import { computed, ref } from 'vue';
import ProgramDetails from './ProgramDetails.vue';

const props = defineProps(['talk', 'day-start', 'height', 'hour-width']);
const showModal = ref(false);

const left = computed(() => {
  return ((props.talk.start.getTime() - props.dayStart.getTime()) / 3600_000) * props.hourWidth + 2;
});

const width = computed(() => {
  return ((props.talk.end.getTime() - props.talk.start.getTime()) / 3600_000) * props.hourWidth - 2;
});

const start = computed(() => formatTime(props.talk.start));
const end = computed(() => formatTime(props.talk.end));

const bgClasses = computed(() => {
  const type = props.talk.type.toLowerCase();
  if (type.includes('kongresa temo')) {
    return { topic: true };
  }
  if (type.includes('scienc')) {
    return { science: true };
  }
  if (type.includes('libroservo')) {
    return { libroservo: true };
  }
  switch (type) {
    case 'kurso':
      return { kurso: true };
    case 'kleriga lundo':
      return { kleriga: true };
    case 'tago de lernado':
      return { lernado: true };
  }
  return {};
});
</script>

<style scoped lang="scss">
.talk {
  margin-top: 1px;
  border-radius: 3px;
  color: #222;
  background-color: #def3dd;
  position: absolute;
  box-sizing: border-box;
  padding: 3px;
  overflow: hidden;
  cursor: pointer;
  transition: background 140ms;

  &:hover {
    background: darken(#def3dd, 10%);
  }

  &.topic {
    background: #ffebe8;

    &:hover {
      background: darken(#ffebe8, 10%);
    }
  }

  &.kurso {
    background: #e0f3fe;

    &:hover {
      background: darken(#e0f3fe, 10%);
    }
  }

  &.science {
    background: #fffaea;

    &:hover {
      background: darken(#fffaea, 10%);
    }
  }

  &.kleriga {
    background: #e7d7f8;

    &:hover {
      background: darken(#e7d7f8, 10%);
    }
  }

  &.libroservo {
    background: #f7edda;

    &:hover {
      background: darken(#f7edda, 10%);
    }
  }

  &.lernado {
    background: #fad6ff;

    &:hover {
      background: darken(#fad6ff, 10%);
    }
  }
}

.info {
  white-space: nowrap;
  font-size: 0.9em;
  overflow: hidden;
  text-overflow: ellipsis;

  .hour {
    font-weight: bold;
  }
}

.title {
  font-weight: bold;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.speakers {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.liked {
  position: absolute;
  top: 1px;
  right: 4px;
  color: #fa5454;
  text-shadow: 0 0 2px #000000a8;
}
</style>
