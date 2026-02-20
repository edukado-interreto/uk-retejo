<template>
  <n-h1>Listo de aliĝintoj</n-h1>
  <n-card v-if="participants === null" class="custom-card" title="Sekurecdemando">
    <p style="margin-top: 0">En kiu jaro okazos la 111-a UK en Graz?</p>

    <n-input-group>
      <n-input type="text" size="large" style="width: 16em" v-model:value="year" @keydown.enter="fetchData" />
      <n-button size="large" type="primary" :loading="loading" @click="fetchData"> Sendi </n-button>
    </n-input-group>
  </n-card>
  <template v-else>
    <p>
      {{ participants.length }} personoj el {{ numberOfCountries }} landoj jam aliĝis al la 111-a Universala Kongreso de
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
      <n-table :single-line="false" striped size="small">
        <thead>
          <tr>
            <th>Nomo</th>
            <th>Lando</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(participant, index) in filteredListByName" :key="index">
            <td v-if="participant.hidden" class="hidden">Kaŝita</td>
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
        class="custom-card"
        :title="`${country.flag} ${country.name} (${country.participants.length + country.hidden})`"
      >
        <ul v-if="country.participants.length > 0" style="margin: 0">
          <li v-for="(participant, index2) in country.participants" :key="index2">
            {{ participant.first_name }}
            <strong>{{ participant.last_name }}</strong>
          </li>
        </ul>
        <p v-if="country.hidden === 1">
          Unu {{ country.participants.length > 0 ? 'alia ' : '' }}partoprenanto el {{ country.name }} ne konsentis aperi
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

<script>
import { NInputGroup } from 'naive-ui';
import axios from 'axios';
import { useMessage } from 'naive-ui';
import { mapGetters } from 'vuex';

export default {
  name: 'RegisteredParticipants',
  components: { NInputGroup },
  data() {
    return {
      year: '',
      loading: false,
      message: useMessage(),
      participants: null,
      modeName: true,
      filterLetter: null,
      filterCountry: null,
    };
  },
  computed: {
    ...mapGetters(['countries']),
    numberOfCountries() {
      if (this.participants === null) {
        return 0;
      }
      const countries = this.participants.map((p) => p.country).filter((c) => c in this.countries);

      let uniqueCount = 0;
      countries.forEach((element, index) => {
        if (countries.indexOf(element) === index) {
          uniqueCount += 1;
        }
      });
      return uniqueCount;
    },
    listByName() {
      const listWithCountries = this.participants.map((p) => {
        return {
          ...p,
          country: p.country in this.countries ? this.countries[p.country].name : p.country,
        };
      });
      const notHidden = listWithCountries
        .filter((p) => !p.hidden)
        .sort(function (a, b) {
          if (a.last_name === b.last_name) {
            return Intl.Collator('eo').compare(a.first_name, b.first_name);
          }
          return Intl.Collator('eo').compare(a.last_name, b.last_name);
        });
      const hidden = listWithCountries
        .filter((p) => p.hidden)
        .sort(function (a, b) {
          return Intl.Collator('eo').compare(a.country, b.country);
        });
      return [...notHidden, ...hidden];
    },
    filteredListByName() {
      if (this.filterLetter === null) {
        return this.listByName;
      }
      return this.listByName.filter(
        (p) => !p.hidden && this.assignLetter(p.last_name.charAt(0).toUpperCase()) === this.filterLetter,
      );
    },
    firstLetters() {
      const letters = [];
      this.participants.forEach((p) => {
        if (!p.hidden) {
          const letter = this.assignLetter(p.last_name.charAt(0).toUpperCase());
          if (!letters.includes(letter)) {
            letters.push(letter);
          }
        }
      });
      letters.sort(function (a, b) {
        return Intl.Collator('eo').compare(a, b);
      });
      return letters;
    },
    listByCountry() {
      const uniqueCountries = [];
      this.participants.forEach((p) => {
        if (p.country in this.countries && !uniqueCountries.includes(p.country)) {
          uniqueCountries.push(p.country);
        }
      });

      const countries = [];
      const otherCountries = [];
      uniqueCountries.forEach((c) => {
        const hidden = this.participants.filter((p) => p.country === c && p.hidden).length;
        const participants = this.participants
          .filter((p) => p.country === c && !p.hidden)
          .sort(function (a, b) {
            if (a.last_name === b.last_name) {
              return Intl.Collator('eo').compare(a.first_name, b.first_name);
            }
            return Intl.Collator('eo').compare(a.last_name, b.last_name);
          });
        if (c in this.countries) {
          const country = {
            code: c,
            name: this.countries[c].name,
            flag: this.flagEmoji(c),
            participants,
            hidden,
          };
          countries.push(country);
        } else {
          const country = {
            code: c,
            name: 'Forpasintoj',
            flag: '',
            participants,
            hidden,
          };
          otherCountries.push(country);
        }
      });

      countries.sort(function (a, b) {
        return Intl.Collator('eo').compare(a.name, b.name);
      });

      return [...countries, ...otherCountries];
    },
    filteredListByCountry() {
      if (this.filterCountry === null) {
        return this.listByCountry;
      }
      return this.listByCountry.filter((c) => c.code === this.filterCountry);
    },
  },
  methods: {
    assignLetter(letter) {
      const substitutions = {
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
      if (letter in substitutions) {
        return substitutions[letter];
      }
      return letter;
    },
    fetchData() {
      this.loading = true;
      axios
        .post('/participants', { year: this.year })
        .then((result) => {
          if (result.data.success) {
            this.participants = result.data.participants;
          } else {
            this.message.error('Malĝusta respondo.', {
              keepAliveOnHover: true,
            });
          }
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
.n-table th {
  font-weight: bold;
}

.hidden {
  font-style: italic;
  color: #777;
}

.buttonsList {
  text-align: center;
  margin: 2rem 0;
}

.buttonsList button {
  margin: 0.3rem;
}
</style>
