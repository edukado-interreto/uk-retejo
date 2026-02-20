<template>
  <n-h4>Invitilo</n-h4>

  <form-invitation
    :default-name="(defaultData.persona_nomo + ' ' + defaultData.familia_nomo).trim()"
    :default-country="defaultData.lando"
    :default-birthdate="defaultData.naskigxdato"
  />

  <n-h4>Bankedo</n-h4>
  <n-p>
    La ĉi-jara bankedo havos formon de bufedo, kie oni mem iros elekti kaj surtelerigi manĝojn laŭ sia prefero.<br />
    La bufedo enhavos diversajn pladojn, kiuj taŭgos por viandmanĝantoj, vegetaranoj kaj veganoj. Pli da informoj en la
    <router-link :to="{ name: 'duaBulteno' }">Dua Bulteno</router-link>.
  </n-p>
  <radio-input v-model="form.bankedo" field-name="bankedo" :options="formOptions.banquet" vertical />
  <slide-transition>
    <radio-input
      v-if="form.bankedo === formOptions.boolValues.yes"
      v-model="form.bankedo_tipo"
      field-name="bankedo_tipo"
      :options="['kunviande', 'vegetare', 'vegane']"
      vertical
      required
      help="Via elekto helpos al ni plani la ĝustajn kvantojn de manĝaĵoj laŭ la manĝotipoj."
    />
  </slide-transition>

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

<script>
import RadioInput from '@/components/form/fields/RadioInput.vue';
import FormTrips from '@/components/form/parts/booking/trips/FormTrips.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import { mapGetters } from 'vuex';
import FormInvitation from '@/components/form/parts/booking/FormInvitation.vue';
import FormHotels from '@/components/form/parts/booking/FormHotels.vue';
import FormPrePostTrips from '@/components/form/parts/booking/FormPrePostTrips.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import FormBookingPrice from '@/components/form/parts/booking/FormBookingPrice.vue';
import CheckboxInput from '@/components/form/fields/CheckboxInput.vue';

export default {
  components: {
    CheckboxInput,
    FormBookingPrice,
    FormInvitation,
    FormTrips,
    TextInput,
    FormHotels,
    FormPrePostTrips,
    SlideTransition,
    RadioInput,
  },
  props: {
    modelValue: {
      type: Object,
      required: true,
    },
    defaultData: {
      // Data already picked by user before loading the form
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
  },
  emits: ['update:modelValue'],
  name: 'FormBooking',
  computed: {
    ...mapGetters(['formOptions']),
    form: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
  mounted() {
    this.scrollTo('mendilo', 12);
  },
};
</script>

<style scoped></style>
