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
      (MA aŭ MA-T). <em>Aligitaj membroj eniras kategorion 2, kiam temas pri kongresa kotizo.</em>
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

  <n-h4>Aliĝkategorio</n-h4>
  <ul>
    <li><strong>A-landoj:</strong> {{ aCountries }}</li>
    <li><strong>B-landoj:</strong> {{ bCountries }}</li>
  </ul>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'PriceTable',
  data() {
    return {
      aligxtipoj: [],
      countryCategory: null,
    };
  },
  computed: {
    ...mapGetters(['currentPeriod', 'registrationPeriods', 'prices', 'countries', 'formOptions']),
    aCountries() {
      return this.countriesByCategory('A');
    },
    bCountries() {
      return this.countriesByCategory('B');
    },
    lastPeriod() {
      const date = new Date(this.registrationPeriods[this.registrationPeriods.length - 1]);
      date.setDate(date.getDate() + 1); // Add 1 day
      return date.toISOString().split('T')[0];
    },
    periods() {
      return [
        'Ĝis ' + this.registrationPeriods[0],
        'Ĝis ' + this.registrationPeriods[1],
        'Ĝis ' + this.registrationPeriods[2],
        'Ekde ' + this.lastPeriod,
      ];
    },
  },
  methods: {
    countriesByCategory(cat) {
      return Object.values(this.countries)
        .filter((c) => c.category === cat)
        .map((c) => c.name)
        .sort(function (a, b) {
          return Intl.Collator('eo').compare(a, b);
        })
        .join(', ');
    },
  },
  created() {
    this.aligxtipoj = [
      {
        title: '1. Individua membro de UEA (ne inkluzivas aligitajn membrojn)',
        prices: this.prices.participation.baza.price[0],
      },
      {
        title: '2. Ne individua membro de UEA',
        prices: this.prices.participation.baza.price[1],
      },
      {
        title: '3. Komitatano / kunulo / junulo / handikapulo, mem individua membro de UEA',
        prices: this.prices.participation.komitatano.price[0],
      },
      {
        title: '4. Kunulo / junulo / handikapulo, ne individua membro de UEA',
        prices: this.prices.participation.junulo.price[1],
      },
    ];
  },
};
</script>

<style scoped>
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
  background-color: #ccffcc;
}
</style>
