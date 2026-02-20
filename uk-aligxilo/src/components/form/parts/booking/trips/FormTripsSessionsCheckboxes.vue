<template>
  <n-checkbox-group v-model:value="modelValue" style="margin-top: 8px">
    <n-space vertical>
      <n-checkbox
        v-for="session in sessions2"
        :key="session.id"
        :value="session.id"
        :disabled="disabledTrips.includes(session.id)"
      >
        <span v-html="session.name"></span>
      </n-checkbox>
    </n-space>
  </n-checkbox-group>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  sessions: Array,
  fullTrips: Array,
  disabledTrips: Array,
});

const modelValue = defineModel('modelValue');

const sessions2 = computed(() =>
  props.sessions.map((s) => {
    let name = s.name;
    if (props.fullTrips.includes(s.id)) {
      name += ' <span style="color: #ff2626">(plena!)</span>';
    }
    return {
      ...s,
      name,
    };
  }),
);
</script>
