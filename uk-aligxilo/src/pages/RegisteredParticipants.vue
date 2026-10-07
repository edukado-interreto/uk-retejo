<template>
  <n-h1>Listo de aliĝintoj</n-h1>
  <n-card v-if="participants === null" class="custom-card" title="Sekurecdemando">
    <p style="margin-top: 0">En kiu jaro okazos la 112-a UK en Melburno?</p>

    <n-input-group>
      <n-input type="text" size="large" style="width: 16em" v-model:value="year" @keydown.enter="fetchData" />
      <n-button size="large" type="primary" :loading="loading" @click="fetchData">Sendi</n-button>
    </n-input-group>
  </n-card>
  <template v-else>
    <p>
      {{ participants.length }} personoj el {{ numberOfCountries }} landoj jam aliĝis al la 112-a Universala Kongreso de
      Esperanto.
    </p>
    <div style="text-align: center; margin: 2rem 0">
      <n-input-group style="width: auto">
        <n-button size="large" :type="modeName ? 'primary' : 'default'" @click="modeName = true">
          Laŭnoma listo
        </n-button>
        <n-button size="large" :type="modeName ? 'default' : 'primary'" @click="modeName = false">
          Laŭlanda listo
        </n-button>
      </n-input-group>
    </div>

    <template v-if="modeName">
      <div class="buttonsList">
        <n-button :type="filterLetter === null ? 'primary' : 'default'" @click="filterLetter = null"> Ĉiuj </n-button>
        <n-button
          v-for="letter in firstLetters"
          :key="letter"
          :type="filterLetter === letter ? 'primary' : 'default'"
          @click="filterLetter = letter"
        >
          {{ letter }}
        </n-button>
      </div>
      <n-table :single-line="false" striped size="small" style="max-width: 800px; margin: auto">
        <thead>
          <tr>
            <th>Nomo</th>
            <th>Lando</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(participant, index) in filteredListByName" :key="index">
            <td v-if="participant.hidden" class="participant-hidden">Kaŝita</td>
            <td v-else>
              {{ participant.first_name }}
              <strong>{{ participant.last_name }}</strong>
            </td>
            <td>{{ participant.country }}</td>
          </tr>
        </tbody>
      </n-table>
    </template>
    <template v-else>
      <div class="buttonsList">
        <n-button :type="filterCountry === null ? 'primary' : 'default'" @click="filterCountry = null"> Ĉiuj </n-button>
        <n-button
          v-for="country in listByCountry"
          :key="country.code"
          :type="filterCountry === country.code ? 'primary' : 'default'"
          @click="filterCountry = country.code"
        >
          {{ country.flag }} {{ country.name }} ({{ country.participants.length + country.hidden }})
        </n-button>
      </div>

      <n-card
        v-for="(country, index) in filteredListByCountry"
        :key="index"
        class="custom-card country-card"
        :title="`${country.flag} ${country.name} (${country.participants.length + country.hidden})`"
      >
        <ul v-if="country.participants.length > 0" style="margin: 0">
          <li v-for="(participant, index2) in country.participants" :key="index2">
            {{ participant.first_name }}
            <strong>{{ participant.last_name }}</strong>
          </li>
        </ul>
        <p v-if="country.hidden === 1">
          1 {{ country.participants.length > 0 ? 'alia ' : '' }}partoprenanto el {{ country.name }} ne konsentis aperi
          en la publika listo de partoprenantoj.
        </p>
        <p v-else-if="country.hidden > 1">
          {{ country.hidden }} {{ country.participants.length > 0 ? 'aliaj ' : '' }}partoprenantoj el
          {{ country.name }} ne konsentis aperi en la publika listo de partoprenantoj.
        </p>
      </n-card>
    </template>
  </template>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { NInputGroup, useMessage } from 'naive-ui';
import axios from 'axios';
import { flagEmoji } from '@/helpers/functions';

defineOptions({ name: 'RegisteredParticipants' });

const store = useStore();
const message = useMessage();

const year = ref('');
const loading = ref(false);
const participants = ref(null);
const modeName = ref(true);
const filterLetter = ref(null);
const filterCountry = ref(null);

const countries = computed(() => store.getters.countries);

const collator = Intl.Collator('eo');

function compareByName(a, b) {
  if (a.last_name === b.last_name) {
    return collator.compare(a.first_name, b.first_name);
  }
  return collator.compare(a.last_name, b.last_name);
}

const letterSubstitutions = {
  Č: 'Ĉ',
  Š: 'Ŝ',
  Ş: 'Ŝ',
  Ș: 'Ŝ',
  Ś: 'S',
  Ł: 'L',
  Ž: 'Z',
  Ż: 'Z',
  Ź: 'Z',
  É: 'E',
  Å: 'A',
  Á: 'A',
  İ: 'I',
  Í: 'I',
  Ó: 'O',
  Ö: 'O',
  Ü: 'U',
};

function assignLetter(letter) {
  return letterSubstitutions[letter] ?? letter;
}

function firstLetter(participant) {
  return assignLetter(participant.last_name.charAt(0).toUpperCase());
}

const numberOfCountries = computed(() => {
  if (participants.value === null) {
    return 0;
  }
  return new Set(participants.value.map((p) => p.country).filter((c) => c in countries.value)).size;
});

const listByName = computed(() => {
  const listWithCountries = participants.value.map((p) => ({
    ...p,
    country: p.country in countries.value ? countries.value[p.country].name : p.country,
  }));
  const notHidden = listWithCountries.filter((p) => !p.hidden).sort(compareByName);
  const hidden = listWithCountries.filter((p) => p.hidden).sort((a, b) => collator.compare(a.country, b.country));
  return [...notHidden, ...hidden];
});

const filteredListByName = computed(() => {
  if (filterLetter.value === null) {
    return listByName.value;
  }
  return listByName.value.filter((p) => !p.hidden && firstLetter(p) === filterLetter.value);
});

const firstLetters = computed(() => {
  const letters = new Set(participants.value.filter((p) => !p.hidden).map(firstLetter));
  return [...letters].sort((a, b) => collator.compare(a, b));
});

const listByCountry = computed(() => {
  const uniqueCountries = new Set(participants.value.map((p) => p.country).filter((c) => c in countries.value));

  const knownCountries = [];
  const otherCountries = [];
  uniqueCountries.forEach((c) => {
    const hidden = participants.value.filter((p) => p.country === c && p.hidden).length;
    const countryParticipants = participants.value.filter((p) => p.country === c && !p.hidden).sort(compareByName);
    if (c in countries.value) {
      knownCountries.push({
        code: c,
        name: countries.value[c].name,
        flag: flagEmoji(c),
        participants: countryParticipants,
        hidden,
      });
    } else {
      otherCountries.push({
        code: c,
        name: 'Forpasintoj',
        flag: '',
        participants: countryParticipants,
        hidden,
      });
    }
  });

  knownCountries.sort((a, b) => collator.compare(a.name, b.name));

  return [...knownCountries, ...otherCountries];
});

const filteredListByCountry = computed(() => {
  if (filterCountry.value === null) {
    return listByCountry.value;
  }
  return listByCountry.value.filter((c) => c.code === filterCountry.value);
});

async function fetchData() {
  loading.value = true;
  try {
    const result = await axios.post('/participants', { year: year.value });
    if (result.data.success) {
      participants.value = result.data.participants;
    } else {
      message.error('Malĝusta respondo.', { keepAliveOnHover: true });
    }
  } catch (error) {
    message.error(String(error), { keepAliveOnHover: true });
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped lang="scss">
.n-table th {
  font-weight: bold;

  td,
  th {
    padding-left: 8px;
  }
}

.participant-hidden {
  font-style: italic;
  color: #7a7a7a;
}

.n-card.custom-card.country-card {
  max-width: 760px;
  margin-left: auto;
  margin-right: auto;

  p {
    margin-top: 1em;
    margin-bottom: 0;
  }
}

.buttonsList {
  margin: 2rem 0;
}

.buttonsList button {
  margin: 0.3rem;
}
</style>
