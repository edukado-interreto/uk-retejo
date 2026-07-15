<template>
  <congress-header />

  <n-h2>Kongresa aliĝilo</n-h2>
  <main-form :default-data="form" />
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import MainForm from '../components/MainForm.vue';
import CongressHeader from '@/components/layout/CongressHeader.vue';

const form = ref({
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
  partopreno_de: null,
  partopreno_gxis: null,
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
});

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);

function isTodayInRange(startStr, endStr) {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  const todayStr = `${yyyy}-${mm}-${dd}`;

  const current = new Date(todayStr);
  const start = new Date(startStr);
  const end = new Date(endStr);

  return current >= start && current <= end;
}

if (isTodayInRange(formOptions.value.congressStart, formOptions.value.congressEnd)) {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  form.value.partopreno_de = `${yyyy}-${mm}-${dd}`;
} else {
  form.value.partopreno_de = formOptions.value.congressStart;
}
form.value.partopreno_gxis = formOptions.value.congressEnd;
</script>
