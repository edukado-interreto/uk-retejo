<template>
  <n-modal v-model:show="showModal" style="max-width: 700px" preset="card" :title="talk.title" size="medium">
    <div class="meta">
      <div><n-switch v-model:value="liked" /> &nbsp;Ŝati la programeron</div>
      <div>
        <n-icon :size="iconSize">
          <location-outline color="#333" />
        </n-icon>
        {{ talk.place }}
      </div>

      <div>
        <n-icon :size="iconSize">
          <time-outline />
        </n-icon>
        {{ date }}
      </div>

      <div v-if="talk.type">
        <n-icon :size="iconSize">
          <help-circle-outline />
        </n-icon>
        {{ talk.type }}
      </div>
      <div v-if="talk.speakers">
        <n-icon :size="iconSize">
          <person-outline />
        </n-icon>
        {{ talk.speakers }}
      </div>
    </div>
    <div class="description" v-if="talk.description" v-html="talk.description"></div>

    <template #footer>
      <n-button type="primary" @click="showModal = false">Fermi</n-button>
    </template>
  </n-modal>
</template>

<script setup>
import { formatTime, formatDateString, dayOfWeekEO } from '@/helpers/time.js';
import { computed } from 'vue';
import { NIcon, NSwitch } from 'naive-ui';
import { LocationOutline, TimeOutline, HelpCircleOutline, PersonOutline } from '@vicons/ionicons5';
import { useLocalStorage } from '@vueuse/core';

const props = defineProps({
  talk: Object,
  show: Boolean,
});

const emit = defineEmits(['close']);
const iconSize = 24;

const showModal = computed({
  get() {
    return props.show;
  },
  set(v) {
    if (!v) {
      emit('close');
    }
  },
});

const date = computed(
  () =>
    `${dayOfWeekEO(props.talk.day, true)}n la ${formatDateString(props.talk.day, true)}, de ${formatTime(
      props.talk.start
    )} ĝis ${formatTime(props.talk.end)}`
);

const storage = useLocalStorage('ukLikedTalks', []);

const liked = computed({
  get() {
    return storage.value.includes(props.talk.id);
  },
  set(newVal) {
    if (newVal) {
      storage.value.push(props.talk.id);
    } else {
      storage.value = storage.value.filter((i) => i !== props.talk.id);
    }
  },
});
</script>

<style scoped lang="scss">
.meta {
  div {
    margin-bottom: 4px;
  }

  .n-icon {
    position: relative;
    top: 6px;
    padding-right: 4px;
  }
}

.description {
  text-align: justify;
  margin-top: 1rem;
}
</style>
