<script setup>
import { ref, watch } from 'vue';
import { NConfigProvider } from 'naive-ui';
import { useKotizoj, useMediaQuery } from './useKotizoj';
import PersonaBox from './PersonaBox.vue';
import PriceTable from './PriceTable.vue';
import PeriodCards from './PeriodCards.vue';
import TableNotes from './TableNotes.vue';
import EligibilityCards from './EligibilityCards.vue';
import MoreInfo from './MoreInfo.vue';
import CountryLists from './CountryLists.vue';
import './kotizoj.css';

const props = defineProps({
  /** Datumoj de la kongreso, konstruitaj el la datumoj de la aliĝilo (vidu src/pages/PriceTable.vue). */
  data: { type: Object, required: true },
  /** Indekso de la nuna aliĝperiodo, kalkulita de la servilo. */
  currentPeriod: { type: Number, default: null },
  /** Oficiala nomo de la lando rekonita ĉe la servilo, aŭ null. */
  detectedCountry: { type: String, default: null },
});

const country = ref(props.detectedCountry);
watch(
  () => props.detectedCountry,
  (v) => {
    if (v && !country.value) country.value = v;
  },
);

const { periods, nowIndex, category, countryOptions, texts, price } = useKotizoj(
  () => props.data,
  () => props.currentPeriod,
  country,
);
const isMobile = useMediaQuery('(max-width: 767px)');

const themeOverrides = {
  common: {
    primaryColor: '#006045',
    primaryColorHover: '#007a55',
    primaryColorPressed: '#004230',
    primaryColorSuppl: '#007a55',
    fontFamily: 'inherit',
    borderRadius: '12px',
  },
};
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides" abstract>
    <div class="kt-page">
      <p class="kt-lead">
        Ju pli frue vi aliĝas kaj pagas, des malpli vi pagas. La aliĝilo aŭtomate kalkulas vian kotizon.
      </p>

      <PersonaBox
        v-model:country="country"
        :category="category"
        :period="periods[nowIndex]"
        :is-last="nowIndex === periods.length - 1"
        :options="countryOptions"
        :aligxilo-url="data.aligxiloUrl"
      />

      <section class="kt-section kt-section--prices" aria-labelledby="kt-h-kotizoj">
        <h2 id="kt-h-kotizoj" class="kt-h2">Kotizoj laŭ aliĝperiodo</h2>
        <PeriodCards
          v-if="isMobile"
          :periods="periods"
          :now-index="nowIndex"
          :category="category"
          :texts="texts"
          :price="price"
        />
        <PriceTable
          v-else
          :periods="periods"
          :now-index="nowIndex"
          :category="category"
          :texts="texts"
          :price="price"
        />
        <TableNotes :is-mobile="isMobile" />
      </section>

      <EligibilityCards :junulo="data.junulo" :senpage-post="data.senpage_post" />
      <MoreInfo />
      <CountryLists :landoj-a="data.landoj_A" :landoj-b="data.landoj_B" />

      <p class="kt-contact">Demandoj? Skribu al <a href="mailto:kongresoj@co.uea.org">kongresoj@co.uea.org</a>.</p>
    </div>
  </n-config-provider>
</template>
