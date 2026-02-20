<template>
  <table>
    <tbody>
      <tr v-if="banquetPrice > 0">
        <td>Bankedo</td>
        <td></td>
        <td>{{ banquetPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="hotelPrice > 0">
        <td>Hotelo</td>
        <td>
          {{ hotelName }}<br />
          {{ roomPrice }}&nbsp;€ × {{ peopleInRoom }} persono{{ j(peopleInRoom) }} × {{ nights }} nokto{{ j(nights) }}
        </td>
        <td>{{ hotelPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="preCongressPrice > 0">
        <td>Antaŭkongresa ekskurso</td>
        <td>
          {{ preCongressName }}<br />
          {{ preCongressPriceForOne }}&nbsp;€ × {{ preCongressPeople }} persono{{ j(preCongressPeople) }}
        </td>
        <td>{{ preCongressPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="postCongressPrice > 0">
        <td>Postkongresa ekskurso</td>
        <td>
          {{ postCongressName }}<br />
          {{ postCongressPriceForOne }}&nbsp;€ × {{ postCongressPeople }} persono{{ j(postCongressPeople) }}
        </td>
        <td>{{ postCongressPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="tripsPrice > 0">
        <td>Ekskursoj</td>
        <td>
          <ul>
            <li v-for="(price, name, index) in tripsWithPrices" :key="index">{{ name }}<br />{{ price }}&nbsp;€</li>
          </ul>
        </td>
        <td>{{ tripsPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="transportationPrice > 0">
        <td>Semajna bileto por publika transporto</td>
        <td></td>
        <td>{{ transportationPrice }}&nbsp;€</td>
      </tr>
      <tr v-if="form.sumo_rabato_mendo > 0">
        <td>Rabato por la mendo</td>
        <td></td>
        <td>{{ form.sumo_rabato_mendo * -1 }}&nbsp;€</td>
      </tr>
      <tr v-if="form.sumo_malrabato_mendo > 0">
        <td>Krompago por la mendo</td>
        <td></td>
        <td>{{ form.sumo_malrabato_mendo }}&nbsp;€</td>
      </tr>
      <tr class="sum">
        <td>Sumo</td>
        <td></td>
        <td>{{ sum }}&nbsp;€</td>
      </tr>
      <template v-if="form.sumo_mendo_pagita">
        <tr class="sum">
          <td>Jam pagita sumo</td>
          <td></td>
          <td>{{ form.sumo_mendo_pagita }}&nbsp;€</td>
        </tr>
        <tr class="sum">
          <td>{{ form.sumo_mendo_pagita > sum ? 'Repagota' : 'Ankoraŭ pagenda' }} sumo</td>
          <td></td>
          <td>{{ sum - form.sumo_mendo_pagita }}&nbsp;€</td>
        </tr>
      </template>
    </tbody>
  </table>

  <n-p v-if="sum > 0">Detalojn pri pagmanieroj vi ricevos retpoŝte post kontrolo de via mendo.</n-p>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'FormBookingPrice',
  props: {
    form: Object,
  },
  computed: {
    ...mapGetters(['formOptions', 'prices']),

    banquetPrice() {
      if (this.form.bankedo === this.formOptions.boolValues.yes) {
        return this.prices.banquet;
      }
      return 0;
    },

    tripsWithPrices() {
      const trips = {};
      this.formOptions.trips.forEach((t) => {
        t.sessions.forEach((s) => {
          if (this.form.ekskursoj.includes(s.id)) {
            trips[s.fullName] = t.price;
          }
        });
      });
      return trips;
    },
    tripsPrice() {
      return Object.values(this.tripsWithPrices).reduce((a, b) => a + b, 0);
    },

    hotelName() {
      return this.formOptions.hotels[this.form.hotelo].name;
    },
    peopleInRoom() {
      return this.formOptions.hotels[this.form.hotelo].payForRoom
        ? this.formOptions.hotels[this.form.hotelo].rooms[this.form.hotelo_cxambro].people
        : 1;
    },
    roomPrice() {
      return this.formOptions.hotels[this.form.hotelo].rooms[this.form.hotelo_cxambro].price;
    },
    nights() {
      return this.daysBetweenDates(this.form.hotelo_de, this.form.hotelo_gxis);
    },
    hotelPrice() {
      if (this.form.hotelo_cxefmendanto !== '') {
        return 0;
      }
      if (!this.form.hotelo || !this.form.hotelo_cxambro || !this.form.hotelo_de || !this.form.hotelo_gxis) {
        return 0;
      }
      return this.roomPrice * this.peopleInRoom * this.nights;
    },

    preCongressName() {
      return this.formOptions.preposttrips[this.form.ak].name;
    },
    preCongressPriceForOne() {
      const rooms = this.formOptions.preposttrips[this.form.ak].rooms;
      if (!(this.form.ak_cxambro in rooms)) {
        return null;
      }
      return rooms[this.form.ak_cxambro].price;
    },
    preCongressPeople() {
      return this.formOptions.preposttrips[this.form.ak].rooms[this.form.ak_cxambro].people;
    },
    preCongressPrice() {
      if (this.form.ak_cxefmendanto !== '') {
        return 0;
      }
      if (!this.form.ak || this.preCongressPriceForOne === null) {
        return 0;
      }
      return this.preCongressPriceForOne * this.preCongressPeople;
    },

    postCongressName() {
      return this.formOptions.preposttrips[this.form.pk].name;
    },
    postCongressPriceForOne() {
      const rooms = this.formOptions.preposttrips[this.form.pk].rooms;
      if (!(this.form.pk_cxambro in rooms)) {
        return null;
      }
      return rooms[this.form.pk_cxambro].price;
    },
    postCongressPeople() {
      return this.formOptions.preposttrips[this.form.pk].rooms[this.form.pk_cxambro].people;
    },
    postCongressPrice() {
      if (this.form.pk_cxefmendanto !== '') {
        return 0;
      }
      if (!this.form.pk || this.postCongressPriceForOne === null) {
        return 0;
      }
      return this.postCongressPriceForOne * this.postCongressPeople;
    },

    transportationPrice() {
      if ('transporta_bileto' in this.form && this.form.transporta_bileto) {
        return this.prices.transportation;
      }
      return 0;
    },

    sum() {
      return Math.max(
        0,
        this.banquetPrice +
          this.tripsPrice +
          this.hotelPrice +
          this.preCongressPrice +
          this.postCongressPrice +
          this.transportationPrice -
          this.form.sumo_rabato_mendo +
          this.form.sumo_malrabato_mendo,
      );
    },
  },
  methods: {
    j(n) {
      return n > 1 ? 'j' : '';
    },
    daysBetweenDates(date1, date2) {
      const oneDay = 24 * 60 * 60 * 1000; // Number of milliseconds in a day
      const firstDate = new Date(date1);
      const secondDate = new Date(date2);

      return Math.round(Math.abs((firstDate - secondDate) / oneDay));
    },
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
  font-size: 1.2em;
}

tr {
  vertical-align: top;
}

td {
  padding: 3px;
}

tr:not(:last-child) td {
  border-bottom: 1px solid #d0d0d0;
}

td:not(:first-child) {
  padding-left: 1.6em;
}

td:last-child {
  text-align: right;
}

tr.sum {
  font-size: 1.1em;
  font-weight: bold;
}

ul {
  margin: 0;
  padding: 0;
  list-style-type: none;
}
</style>
