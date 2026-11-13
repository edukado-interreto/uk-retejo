<script setup>
import { NCollapse, NCollapseItem } from 'naive-ui';

defineProps({
  landojA: { type: Array, required: true },
  landojB: { type: Array, required: true },
});
</script>

<template>
  <section id="kt-landoj" class="kt-section" aria-labelledby="kt-h-landoj">
    <h2 id="kt-h-landoj" class="kt-h2">Landokategorioj</h2>
    <p class="kt-text">
      Via lando estas la lando, en kiu vi loĝas la plej grandan parton de la jaro, ne nepre via ŝtataneco.
    </p>
    <n-collapse class="kt-lists">
      <n-collapse-item title="A-landoj" name="A">
        <p class="kt-text">{{ landojA.join(', ') }}.</p>
      </n-collapse-item>
      <n-collapse-item title="B-landoj (ĉiuj ceteraj)" name="B">
        <p class="kt-text">{{ landojB.join(', ') }}.</p>
      </n-collapse-item>
    </n-collapse>
  </section>
</template>
