<template>
  <partner-discount-codes />

  <n-h4>Invitilo</n-h4>
  <form-invitation v-model="form" />
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { scrollTo } from '@/helpers/functions.js';
import FormInvitation from '@/components/form/parts/booking/FormInvitation.vue';
import PartnerDiscountCodes from './booking/PartnerDiscountCodes.vue';

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
