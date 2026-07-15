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
          {{ preCongressName }}
          <template v-if="preCongressHasRooms">
            <br />
            {{ preCongressPriceForOne }}&nbsp;€ × {{ preCongressPeople }} persono{{ j(preCongressPeople) }}
          </template>
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

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { daysBetweenDates } from '@/helpers/time.js';

const props = defineProps({
  form: Object,
});

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const prices = computed(() => store.getters.prices);

const banquetPrice = computed(() => {
  if (props.form.bankedo && props.form.bankedo !== formOptions.value.boolValues.no) {
    return prices.value.banquet[props.form.bankedo];
  }
  return 0;
});

const tripsWithPrices = computed(() => {
  const trips = {};
  formOptions.value.trips.forEach((t) => {
    t.sessions.forEach((s) => {
      if (props.form.ekskursoj.includes(s.id)) {
        trips[s.fullName] = t.price;
      }
    });
  });
  return trips;
});

const tripsPrice = computed(() => Object.values(tripsWithPrices.value).reduce((a, b) => a + b, 0));

const hotelName = computed(() => {
  return formOptions.value.hotels[props.form.hotelo]?.name;
});

const peopleInRoom = computed(() => {
  if (!props.form.hotelo) return 1;
  return formOptions.value.hotels[props.form.hotelo].payForRoom
    ? formOptions.value.hotels[props.form.hotelo].rooms[props.form.hotelo_cxambro].people
    : 1;
});

const roomPrice = computed(() => {
  if (!props.form.hotelo || !props.form.hotelo_cxambro) return 0;
  return formOptions.value.hotels[props.form.hotelo].rooms[props.form.hotelo_cxambro].price;
});

const nights = computed(() => {
  return daysBetweenDates(props.form.hotelo_de, props.form.hotelo_gxis);
});

const hotelPrice = computed(() => {
  if (props.form.hotelo_cxefmendanto !== '') {
    return 0;
  }
  if (!props.form.hotelo || !props.form.hotelo_cxambro || !props.form.hotelo_de || !props.form.hotelo_gxis) {
    return 0;
  }
  return roomPrice.value * peopleInRoom.value * nights.value;
});

const preCongressName = computed(() => {
  return formOptions.value.preposttrips[props.form.ak]?.name;
});

const preCongressPriceForOne = computed(() => {
  if (!props.form.ak) return null;
  const rooms = formOptions.value.preposttrips[props.form.ak].rooms;
  if (!(props.form.ak_cxambro in rooms)) {
    return null;
  }
  return rooms[props.form.ak_cxambro].price;
});

const preCongressHasRooms = computed(() => {
  if (!props.form.ak) return false;
  return Object.keys(formOptions.value.preposttrips[props.form.ak].rooms).length > 1;
});

const preCongressPeople = computed(() => {
  if (!props.form.ak || !props.form.ak_cxambro) return 0;
  return formOptions.value.preposttrips[props.form.ak].rooms[props.form.ak_cxambro].people;
});

const preCongressPrice = computed(() => {
  if (props.form.ak && !preCongressHasRooms.value) {
    return formOptions.value.preposttrips[props.form.ak].rooms[''].price;
  }
  if (props.form.ak_cxefmendanto !== '') {
    return 0;
  }
  if (!props.form.ak || preCongressPriceForOne.value === null) {
    return 0;
  }
  return preCongressPriceForOne.value * preCongressPeople.value;
});

const postCongressName = computed(() => {
  return formOptions.value.preposttrips[props.form.pk]?.name;
});

const postCongressPriceForOne = computed(() => {
  if (!props.form.pk) return null;
  const rooms = formOptions.value.preposttrips[props.form.pk].rooms;
  if (!(props.form.pk_cxambro in rooms)) {
    return null;
  }
  return rooms[props.form.pk_cxambro].price;
});

const postCongressPeople = computed(() => {
  if (!props.form.pk || !props.form.pk_cxambro) return 0;
  return formOptions.value.preposttrips[props.form.pk].rooms[props.form.pk_cxambro].people;
});

const postCongressPrice = computed(() => {
  if (props.form.pk_cxefmendanto !== '') {
    return 0;
  }
  if (!props.form.pk || postCongressPriceForOne.value === null) {
    return 0;
  }
  return postCongressPriceForOne.value * postCongressPeople.value;
});

const transportationPrice = computed(() => {
  if ('transporta_bileto' in props.form && props.form.transporta_bileto) {
    return prices.value.transportation;
  }
  return 0;
});

const sum = computed(() => {
  return Math.max(
    0,
    banquetPrice.value +
      tripsPrice.value +
      hotelPrice.value +
      preCongressPrice.value +
      postCongressPrice.value +
      transportationPrice.value -
      (props.form.sumo_rabato_mendo ? parseFloat(props.form.sumo_rabato_mendo) : 0) +
      (props.form.sumo_malrabato_mendo ? parseFloat(props.form.sumo_malrabato_mendo) : 0),
  );
});

function j(n) {
  return n > 1 ? 'j' : '';
}
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
