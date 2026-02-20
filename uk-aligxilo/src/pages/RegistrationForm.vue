<template>
  <congress-header />

  <n-h2>Kongresa aliĝilo</n-h2>
  <main-form :default-data="form" />
</template>

<script>
import MainForm from '../components/MainForm.vue';
import CongressHeader from '@/components/layout/CongressHeader.vue';

export default {
  name: 'RegistrationForm',
  components: { CongressHeader, MainForm },
  data() {
    return {
      form: {
        lando: null,
        uea_kodo: '',
        persona_nomo: '',
        familia_nomo: '',
        genro: null,
        titolo: null,
        naskigxdato: null,
        retadreso: '',
        adreso: '',
        urbo: '',
        posxtkodo: '',
        telefono: '',
        membreco: null,
        kotizo: null,
        cxefaligxinto: '',
        handikapatestilo: null,
        sxildonomo: '',
        sxildolando: '',
        donaco_uk: null,
        donaco_blind: null,
        donaco_iik: null,
        donaco_gepatroj: null,
        donaco_canuto: null,
        donaco_partoprenu_uk: null,
        donaco_co2: null,
        donaco_artaj_aranghoj: null,
        donaco_nourmont: null,
        komento: '',
        kompreno_pago: false,
        konsento_aligxlisto: false,
        konsento_kongreslibro: false,
        kongreslibro_adreso: [],
        konfirmilo: 'elektronike',
        akcepto_reguloj: false,
        pagmaniero: null,
        uea_kodo_paganto: '',

        karto_posedanto: undefined,
        karto_retadreso: undefined,
      },
    };
  },
};
</script>
