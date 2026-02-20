<template>
  <n-flex align="center" justify="center" style="margin-bottom: 1.3em">
    <n-input placeholder="Serĉi laŭ titolo aŭ preleganto" v-model:value="search" clearable style="max-width: 26em">
      <template #prefix>
        <n-icon :component="Search" />
      </template>
    </n-input>
    <n-select
      v-model:value="selectedTypes"
      multiple
      :options="types"
      clearable
      filterable
      placeholder="Serĉi laŭ tipo"
      style="max-width: 20em"
    />
    <div><n-switch v-model:value="liked" /> <span class="sxatataj">Nur ŝatataj</span></div>
    <n-button type="info" :disabled="!resettable" @click="resetFilters">Nuligi filtrilojn</n-button>
  </n-flex>
</template>

<script setup>
import { NIcon, NFlex, NSwitch } from 'naive-ui';
import { Search } from '@vicons/ionicons5';
import { computed } from 'vue';

const props = defineProps({
  types: {
    type: Array,
    required: true,
  },
});

const search = defineModel('search');
const selectedTypes = defineModel('selectedTypes');
const liked = defineModel('liked');

function resetFilters() {
  search.value = '';
  selectedTypes.value = [];
  liked.value = false;
}

const resettable = computed(() => search.value || selectedTypes.value.length || liked.value);
</script>

<style scoped>
.sxatataj {
  color: #797979;
  position: relative;
  top: 2px;
  padding-left: 2px;
}
</style>
