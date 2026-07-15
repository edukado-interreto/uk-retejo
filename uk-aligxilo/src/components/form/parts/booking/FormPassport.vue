<template>
  <n-h4>Datumoj pri via vojaĝdokumento</n-h4>
  <p>Aŭstra leĝo postulas de la hotelo informojn pri via vojaĝdokumento (ekz. pasporto aŭ nacia identigilo).</p>

  <n-grid x-gap="12" cols="1 s:2" responsive="screen">
    <n-gi>
      <select-input
        v-model="form.lando"
        field-name="lando"
        :options="countryOptions"
        placeholder="Elektu landon"
        filterable
        width="20em"
        label="Loĝlando"
      />
    </n-gi>
    <n-gi>
      <select-input
        v-model="form.sxtataneco"
        field-name="sxtataneco"
        :options="countryOptions"
        placeholder="Elektu landon"
        filterable
        width="20em"
      />
    </n-gi>
    <n-gi>
      <text-input v-model="form.pasporto" field-name="pasporto" />
    </n-gi>
    <n-gi>
      <text-input
        v-model="form.eldoninto_pasporto"
        field-name="eldoninto_pasporto"
        help="Ekzakte, kiel indikite sur la dokumento — instanco, kiu eldonis la dokumenton"
      />
    </n-gi>
  </n-grid>
</template>

<script setup>
import { computed } from 'vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import SelectInput from '@/components/form/fields/SelectInput.vue';
import { useStore } from 'vuex';
import { flagEmoji } from '@/helpers/functions';

const form = defineModel();

const store = useStore();
const countries = computed(() => store.getters.countries);

const countryOptions = computed(() =>
  Object.keys(countries.value).map((key) => {
    return { value: key, label: flagEmoji(key) + ' ' + countries.value[key].name };
  }),
);

if (!form.value.sxtataneco) {
  form.value.sxtataneco = form.value.lando;
}
</script>
