<script setup>
import { ref } from 'vue';
import { NSelect } from 'naive-ui';
import { IconArrowUpRight } from '@tabler/icons-vue';
import { normalize } from './useKotizoj';

const props = defineProps({
  country: { type: String, default: null },
  category: { type: String, default: null },
  period: { type: Object, required: true },
  isLast: { type: Boolean, default: false },
  options: { type: Array, required: true },
  aligxiloUrl: { type: String, required: true },
});
const emit = defineEmits(['update:country']);

// Sen rekonita lando la elektilo estas tuj malfermita.
const open = ref(!props.country);

function pick(value) {
  emit('update:country', value);
  open.value = false;
}

const filter = (pattern, option) => normalize(String(option.label)).includes(normalize(pattern));
</script>

<template>
  <section class="kt-persona" aria-label="Via kotizo">
    <div class="kt-persona__text">
      <div class="kt-persona__country">
        <span v-if="country && category" class="kt-persona__title">{{ country }}: landokategorio {{ category }}</span>
        <span v-else class="kt-persona__title">Elektu vian loĝlandon</span>
        <button
          v-if="country"
          type="button"
          class="kt-linkbtn"
          :aria-expanded="open ? 'true' : 'false'"
          aria-controls="kt-lando-elektilo"
          @click="open = !open"
        >
          {{ open ? 'fermi' : 'ŝanĝi landon' }}
        </button>
      </div>

      <label v-if="open" id="kt-lando-elektilo" class="kt-persona__select">
        <span>Elektu vian loĝlandon (la landon, kie vi loĝas la plej grandan parton de la jaro):</span>
        <n-select
          :value="country"
          :options="options"
          :filter="filter"
          filterable
          placeholder="Komencu tajpi la nomon de la lando"
          @update:value="pick"
        />
      </label>

      <p class="kt-persona__period">
        Nun validas la <strong>{{ period.sub }}</strong
        >, <strong>{{ period.longLabel }}</strong
        >.<template v-if="!isLast"> Poste la kotizo altiĝas.</template>
      </p>
    </div>

    <a class="kt-btn" :href="aligxiloUrl"
      >Aliĝi al UK <IconArrowUpRight :size="16" :stroke-width="2.5" aria-hidden="true"
    /></a>
  </section>
</template>
