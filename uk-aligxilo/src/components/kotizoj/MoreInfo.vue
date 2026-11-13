<script setup>
import { IconReceiptEuro, IconBan, IconCircleCheck } from '@tabler/icons-vue';
import RegistrationTimeline from './RegistrationTimeline.vue';

const items = [
  {
    icon: IconReceiptEuro,
    title: 'Kion la kotizo inkluzivas',
    text: 'Partoprenon en la kongresa programo. Ĝi ne inkluzivas loĝadon, manĝojn, ekskursojn, bankedon nek asekuron.',
  },
  {
    icon: IconBan,
    title: 'Repago kaj transdono',
    text: 'La kotizo ne estas repagebla, ankaŭ se vi ne povas partopreni, kaj kongresaneco ne estas transdonebla al alia persono.',
  },
  {
    icon: IconCircleCheck,
    title: 'Kompleta aliĝo',
    text: 'UEA traktas aliĝon nur post ricevo de la aliĝilo kaj kompleta pago. Pagmanieroj estas indikitaj en la aliĝilo.',
  },
];
</script>

<template>
  <section class="kt-section" aria-labelledby="kt-h-pliaj">
    <h2 id="kt-h-pliaj" class="kt-h2">Pliaj informoj</h2>
    <RegistrationTimeline />
    <div class="kt-grid kt-grid--3 kt-info">
      <div v-for="it in items" :key="it.title" class="kt-info__item">
        <div class="kt-cardbox__head">
          <component :is="it.icon" :size="26" :stroke-width="1.8" aria-hidden="true" />
          <h3>{{ it.title }}</h3>
        </div>
        <p>{{ it.text }}</p>
      </div>
    </div>
  </section>
</template>
