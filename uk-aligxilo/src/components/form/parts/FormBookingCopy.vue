<template>
  <n-h4>Invitilo</n-h4>

  <form-invitation v-model="form" />

  <n-h4>Bankedo</n-h4>
  <n-p>
    La bankedo okazos en tipe aŭstra restoracio. Ĝi inkluzivos supon, ĉefpladon, deserton kaj trinkaĵojn. Estos menuoj
    taŭgaj por viandmanĝantoj, vegetaranoj kaj veganoj. Pli da informoj en la
    <router-link :to="{ name: 'duaBulteno' }" target="_blank">Dua Bulteno</router-link>).
  </n-p>
  <radio-input v-model="form.bankedo" field-name="bankedo" :options="formOptions.banquet" vertical />

  <n-h4>Hotelo</n-h4>

  <form-hotels
    v-model="form"
    :default-hotel="defaultData.hotelo"
    :default-room="defaultData.hotelo_cxambro"
    :default-parking="defaultData.parkloko"
  />
  <n-h4>Antaŭkongresa ekskurso</n-h4>

  <form-pre-post-trips v-model="form" :default-trip="defaultData.ak" :default-room="defaultData.ak_cxambro" type="ak" />

  <n-h4>Postkongresa ekskurso</n-h4>

  <form-pre-post-trips v-model="form" :default-trip="defaultData.pk" :default-room="defaultData.pk_cxambro" type="pk" />

  <slide-transition>
    <form-passport v-model="form" v-if="form.hotelo || form.ak_cxambro || form.pk_cxambro" />
  </slide-transition>

  <n-h4>Ekskursoj</n-h4>

  <form-trips :default-trips="defaultData.ekskursoj" v-model="form.ekskursoj" />
  <slide-transition>
    <div v-if="foodTypeRequired" style="margin-top: 2rem">
      <n-h4>Manĝotipo dum ekskursoj</n-h4>
      <radio-input
        v-model="form.mangxotipo"
        field-name="mangxotipo"
        :options="formOptions.foodtypes"
        :required="true"
        label="Bonvolu elekti manĝotipon, kiun vi mendas por la tuttagaj, antaŭ- kaj/aŭ postkongresaj ekskursoj."
      />

      <text-input
        v-if="foodTypeCompanionRequired"
        style="margin-top: 1rem"
        v-model="form.mangxotipo_kunlogxanto"
        field-name="mangxotipo_kunlogxanto"
        required
      />
    </div>
  </slide-transition>

  <n-h4>Komentoj</n-h4>

  <text-input v-model="form.komento_mendo" field-name="komento_mendo" type="textarea" />

  <n-h4>Prezo de la mendo</n-h4>

  <form-booking-price :form="form" />
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { scrollTo } from '@/helpers/functions.js';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import FormTrips from '@/components/form/parts/booking/trips/FormTrips.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import FormInvitation from '@/components/form/parts/booking/FormInvitation.vue';
import FormHotels from '@/components/form/parts/booking/FormHotels.vue';
import FormPrePostTrips from '@/components/form/parts/booking/FormPrePostTrips.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import FormBookingPrice from '@/components/form/parts/booking/FormBookingPrice.vue';
import FormPassport from '@/components/form/parts/booking/FormPassport.vue';

const props = defineProps({
  defaultData: {
    type: Object,
    required: true,
  },
  foodTypeRequired: {
    type: Boolean,
    required: true,
  },
  foodTypeCompanionRequired: {
    type: Boolean,
    required: true,
  },
});

const form = defineModel({ type: Object, required: true });

const store = useStore();

const formOptions = computed(() => store.getters.formOptions);

onMounted(() => {
  scrollTo('mendilo', 12);
});
</script>

<style scoped></style>
