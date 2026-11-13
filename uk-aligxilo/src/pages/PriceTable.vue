<template>
  <kotizoj-page v-if="data" :data="data" :current-period="currentPeriod" :detected-country="detectedCountryName" />
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import KotizojPage from '@/components/kotizoj/KotizojPage.vue';
import { flagEmoji } from '@/helpers/functions';

const store = useStore();

const currentPeriod = computed(() => store.getters.currentPeriod);
const registrationPeriods = computed(() => store.getters.registrationPeriods);
const prices = computed(() => store.getters.prices);
const countries = computed(() => store.getters.countries);
const formOptions = computed(() => store.getters.formOptions);
const detectedCountry = computed(() => store.getters.detectedCountry);

// La servilo liveras la landokodon (ekz. "SK"), la komponanto laboras kun la oficialaj nomoj.
const detectedCountryName = computed(() => countries.value[detectedCountry.value]?.name ?? null);

function countriesByCategory(cat) {
  return Object.values(countries.value)
    .filter((c) => c.category === cat)
    .map((c) => c.name)
    .sort(Intl.Collator('eo').compare);
}

// Prezoj de unu aliĝtipo laŭ landokategorio: { A: [p1, p2, p3, p4], B: [...] }
// membership: 0 = individua membro de UEA, 1 = ne individua membro
function pricesOf(type, membership) {
  const list = prices.value.participation[type].price[membership];
  return { A: list.map((p) => p.A), B: list.map((p) => p.B) };
}

// La datumoj de la aliĝilo en la formo, kiun atendas KotizojPage.
const data = computed(() => {
  if (!prices.value?.participation || !registrationPeriods.value?.length) {
    return null;
  }

  const rows = {
    membro: pricesOf('baza', 0),
    nemembro: pricesOf('baza', 1),
    membro_rabatita: pricesOf('komitatano', 0),
    nemembro_rabatita: pricesOf('junulo', 1),
  };

  return {
    aligxiloUrl: `${import.meta.env.VITE_WEBSITE_URL}/aligxilo`,
    periodoj: [
      ...registrationPeriods.value.map((gxis, i) => ({ numero: i + 1, gxis })),
      { numero: registrationPeriods.value.length + 1, gxis: null },
    ],
    prezoj: Object.fromEntries(
      ['A', 'B'].map((cat) => [cat, Object.fromEntries(Object.entries(rows).map(([key, p]) => [key, p[cat]]))]),
    ),
    junulo: { de: formOptions.value.youthBirthDate, gxis: formOptions.value.childBirthDate },
    senpage_post: formOptions.value.childBirthDate,
    landoj_A: countriesByCategory('A'),
    landoj_B: countriesByCategory('B'),
    // Nomo de la lando → flago, por la elektilo de lando
    flagoj: Object.fromEntries(Object.entries(countries.value).map(([code, c]) => [c.name, flagEmoji(code)])),
  };
});
</script>
