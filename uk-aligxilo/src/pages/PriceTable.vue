<template>
  <n-h1>Partoprenkotizoj por la Universala Kongreso</n-h1>
  <p>
    La kotizo por partopreni en la Universala Kongreso de Esperanto dependas de la dato, kiam vi aliĝas kaj pagas, de
    via lando kaj de la tipo de aliĝkotizo (ekz. ĉu vi estas membro de UEA, ĉu vi estas junulo, ktp.).
  </p>
  <p>La aliĝilo aŭtomate kalkulas vian aliĝkotizon. <strong>Ĉiuj prezoj estas en eŭroj.</strong></p>
  <n-table :single-line="false" size="small">
    <thead>
      <tr>
        <th>Dato de aliĝo kaj pago</th>
        <th v-for="(period, index) in periods" :key="index" :class="{ active: currentPeriod === index }" colspan="2">
          {{ period }}
          <br />
          ({{ index + 1 }}-a aliĝperiodo)
        </th>
      </tr>
      <tr>
        <th>Aliĝkategorio</th>
        <template v-for="(period, index) in periods" :key="index">
          <th :class="{ active: currentPeriod === index && countryCategory === 'A' }">A</th>
          <th :class="{ active: currentPeriod === index && countryCategory === 'B' }">B</th>
        </template>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(type, index) in aligxtipoj" :key="index">
        <th>{{ type.title }}</th>
        <template v-for="(period, i) in type.prices" :key="i">
          <td
            style="text-align: center"
            :class="{ active: i === currentPeriod && (countryCategory === null || countryCategory === 'A') }"
          >
            {{ period.A }}
          </td>
          <td
            style="text-align: center"
            :class="{ active: i === currentPeriod && (countryCategory === null || countryCategory === 'B') }"
          >
            {{ period.B }}
          </td>
        </template>
      </tr>
    </tbody>
  </n-table>

  <n-h4>Difinoj</n-h4>
  <ul>
    <li>
      <strong>Individua membro de UEA</strong>: Dumviva membro (DM aŭ DMJ), Membro Baza (MB aŭ MB-T), Membro-Abonanto
      (MA aŭ MA-T) en la momento de aliĝo.
      <em>Aligitaj membroj eniras kategorion 2, kiam temas pri kongresa kotizo.</em>
    </li>
    <li>
      <strong>Komitatano</strong>: Tiu, kiu estas membro aŭ observanto en la Komitato de UEA en la momento de la aliĝo.
    </li>
    <li>
      <strong>Kunulo</strong>: Tiu, kiu loĝas samadrese kun la ĉefaliĝinto. Ĉefaliĝinto oni konsideras personon, kiu
      pagas kotizon en kategorio 1 aŭ 2.
    </li>
    <li>
      <strong>Junulo</strong>: Tiu, kiu naskiĝis inter {{ formOptions.youthBirthDate }} kaj
      {{ formOptions.childBirthDate }} (inkluzive). Oni nepre notu la naskiĝdaton sur la aliĝilo kaj sendu kopion de
      indentigilo, kie aperas la naskiĝdato.
    </li>
    <li>
      <strong>Handikapulo</strong>: Tiu, kies handikapo nepre postulas akompananton (ekzemple blindulo), kaj kiu pruvis
      tion per kuracista aŭ simila atestilo, kiu klare indikas la tipon de handikapo.
    </li>
  </ul>

  <n-h4>Senpage aliĝas:</n-h4>
  <ul>
    <li>infanoj kaj gejunuloj naskiĝintaj post {{ formOptions.childBirthDate }},</li>
    <li>nemalhaveblaj akompanantoj de handikapuloj.</li>
  </ul>

  <template v-if="prices.earlyDiscounts">
    <n-h4>Rabato pro frua aliĝo</n-h4>
    <p>
      Se vi aliĝas dum la <em>antaŭa</em>, 111-a Universala Kongreso de Esperanto en Graz, t.e. ĝis la 8-a de aŭgusto
      2026, vi ricevas jenan rabaton:
    </p>

    <n-table :single-line="false" size="small" class="discount-table">
      <thead>
        <tr>
          <th>Ĉu vi mem partoprenas en la 111-a UK?</th>
          <th colspan="2">Jes</th>
          <th colspan="2">Ne</th>
        </tr>
        <tr>
          <th>Aliĝkategorio</th>
          <th :class="{ active: countryCategory === 'A' }">A</th>
          <th :class="{ active: countryCategory === 'B' }">B</th>
          <th :class="{ active: countryCategory === 'A' }">A</th>
          <th :class="{ active: countryCategory === 'B' }">B</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(type, index) in aligxtipoj" :key="index">
          <th>{{ type.title }}</th>
          <td style="text-align: center" :class="{ active: countryCategory === 'A' }">
            -{{ type.discount.A + prices.pastParticipantDiscount }}
          </td>
          <td style="text-align: center" :class="{ active: countryCategory === 'B' }">
            -{{ type.discount.B + prices.pastParticipantDiscount }}
          </td>
          <td style="text-align: center" :class="{ active: countryCategory === 'A' }">-{{ type.discount.A }}</td>
          <td style="text-align: center" :class="{ active: countryCategory === 'B' }">-{{ type.discount.B }}</td>
        </tr>
      </tbody>
    </n-table>
  </template>

  <n-h4>Landokategorioj</n-h4>
  <ul>
    <li><strong>A-landoj:</strong> <span v-html="aCountries"></span></li>
    <li><strong>B-landoj:</strong> <span v-html="bCountries"></span></li>
  </ul>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import DOMPurify from 'dompurify';

const store = useStore();

const currentPeriod = computed(() => store.getters.currentPeriod);
const registrationPeriods = computed(() => store.getters.registrationPeriods);
const prices = computed(() => store.getters.prices);
const countries = computed(() => store.getters.countries);
const formOptions = computed(() => store.getters.formOptions);
const detectedCountry = computed(() => store.getters.detectedCountry);

const countryCategory = computed(() => {
  if (!detectedCountry.value) {
    return null;
  }
  const country = countries.value[detectedCountry.value];
  return country ? country.category : null;
});

function countriesByCategory(cat) {
  const list = Object.values(countries.value)
    .filter((c) => c.category === cat)
    .map((c) => (c = c.name))
    .sort(function (a, b) {
      return Intl.Collator('eo').compare(a, b);
    })
    .map((c) => {
      if (
        detectedCountry.value &&
        countries.value[detectedCountry.value] &&
        countries.value[detectedCountry.value].name === c
      ) {
        return `<strong>${c}</strong>`;
      }
      return c;
    })
    .join(', ');
  return DOMPurify.sanitize(list);
}

const aCountries = computed(() => countriesByCategory('A'));
const bCountries = computed(() => countriesByCategory('B'));

const lastPeriod = computed(() => {
  const date = new Date(registrationPeriods.value[registrationPeriods.value.length - 1]);
  date.setDate(date.getDate() + 1); // Add 1 day
  return date.toISOString().split('T')[0];
});
const periods = computed(() => [
  'Ĝis ' + registrationPeriods.value[0],
  'Ĝis ' + registrationPeriods.value[1],
  'Ĝis ' + registrationPeriods.value[2],
  'Ekde ' + lastPeriod.value,
]);

const aligxtipoj = [
  {
    title: '1. Individua membro de UEA (ne inkluzivas aligitajn membrojn)',
    prices: prices.value.participation.baza.price[0],
    discount: prices.value.earlyDiscounts ? prices.value.earlyDiscounts.baza[0] : null,
  },
  {
    title: '2. Ne individua membro de UEA',
    prices: prices.value.participation.baza.price[1],
    discount: prices.value.earlyDiscounts ? prices.value.earlyDiscounts.baza[1] : null,
  },
  {
    title: '3. Komitatano / kunulo / junulo / handikapulo, mem individua membro de UEA',
    prices: prices.value.participation.komitatano.price[0],
    discount: prices.value.earlyDiscounts ? prices.value.earlyDiscounts.komitatano[0] : null,
  },
  {
    title: '4. Kunulo / junulo / handikapulo, ne individua membro de UEA',
    prices: prices.value.participation.junulo.price[1],
    discount: prices.value.earlyDiscounts ? prices.value.earlyDiscounts.junulo[1] : null,
  },
];
</script>

<style scoped lang="scss">
thead th {
  font-weight: bold;
  text-align: center;
}

.n-table th {
  white-space: normal;
}

.n-table td {
  padding: 4px;
}

td.active,
th.active {
  background-color: #bcddfc;
}

ul {
  padding-left: 1.5em;
}

li {
  list-style-type: disc;
}

.discount-table {
  width: auto;
  margin: 2em auto;

  th {
    padding: 4px 8px;
  }

  td {
    padding: 4px 16px;
  }
}
</style>
