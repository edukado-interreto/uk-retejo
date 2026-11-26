<template>
  <div style="margin-bottom: 2.5rem">
    <n-form-item label-placement="left" :show-feedback="false">
      <n-checkbox v-model:checked="invitationNeeded" id="invitationNeeded">
        Mi bezonas invitleteron por vizo
      </n-checkbox>
    </n-form-item>

    <slide-transition>
      <n-card v-if="invitationNeeded" class="custom-card" title="Datumoj por la invitilo">
        <n-grid x-gap="12" y-gap="16" cols="1 m:2" responsive="screen">
          <n-form-item-gi
            label="Nomo de la invitato"
            feedback="Se via nomo ne estas skribita ĝuste tiel en via pasporto, bonvolu kontakti la Kongresan Fakon per kongresoj@co.uea.org."
          >
            <n-input id="invitationName" :value="defaultName" disabled />
          </n-form-item-gi>

          <n-gi>
            <text-input v-model="form.pasporto" field-name="pasporto" label="Pasporta numero" />
          </n-gi>

          <n-form-item-gi label="La pasporto validas ekde" :show-feedback="false">
            <n-date-picker
              v-model:formatted-value="passportValidFrom"
              id="passportValidFrom"
              type="date"
              value-format="yyyy-MM-dd"
            />
          </n-form-item-gi>
          <n-form-item-gi label="La pasporto validas ĝis" :show-feedback="false">
            <n-date-picker
              v-model:formatted-value="passportValidTo"
              id="passportValidTo"
              type="date"
              value-format="yyyy-MM-dd"
            />
          </n-form-item-gi>
          <n-form-item-gi label="Naskiĝdato" :show-feedback="false">
            <n-date-picker
              v-model:formatted-value="birthDate"
              id="birthDate"
              type="date"
              value-format="yyyy-MM-dd"
              :disabled="!!form.naskigxdato"
            />
          </n-form-item-gi>
          <n-gi>
            <select-input
              v-model="form.sxtataneco"
              field-name="sxtataneco"
              :options="countryOptions"
              placeholder="Elektu landon"
              filterable
              width="20em"
              feedback="Bonvolu kontroli kaj korekti, se la loĝlando ne kongruas kun la civitaneco indikita en la pasporto."
            />
          </n-gi>
        </n-grid>
        <div style="text-align: center; padding-top: 2rem">
          <n-button type="info" @click="download" :disabled="!canSubmit" :loading="loading">
            Elŝuti la invitilon
          </n-button>
        </div>
      </n-card>
    </slide-transition>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import { NFormItemGi } from 'naive-ui';
import axios from 'axios';
import downloadFile from 'downloadjs';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import SelectInput from '@/components/form/fields/SelectInput.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import { flagEmoji, registrationIdFromUrl } from '@/helpers/functions';

const form = defineModel({ type: Object, required: true });

const store = useStore();

const invitationNeeded = ref(false);
const passportValidFrom = ref(null);
const passportValidTo = ref(null);
const birthDate = ref(form.value.naskigxdato || null);
const loading = ref(false);
const defaultName = `${form.value.persona_nomo} ${form.value.familia_nomo}`.trim();

if (!form.value.sxtataneco) {
  form.value.sxtataneco = form.value.lando;
}

const countryOptions = computed(() => {
  const countries = store.getters.countries;
  return Object.keys(countries).map((key) => ({ value: key, label: `${flagEmoji(key)} ${countries[key].name}` }));
});

const canSubmit = computed(
  () =>
    form.value.pasporto && passportValidFrom.value && passportValidTo.value && birthDate.value && form.value.sxtataneco,
);

const download = () => {
  loading.value = true;
  return axios
    .post(
      '/invitation',
      {
        id: registrationIdFromUrl(),
        passportNumber: form.value.pasporto,
        passportValidFrom: passportValidFrom.value,
        passportValidTo: passportValidTo.value,
        birthDate: birthDate.value,
        country: form.value.sxtataneco,
      },
      { responseType: 'blob' },
    )
    .then((response) => {
      downloadFile(response.data, `Invitletero ${defaultName}.pdf`);
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped></style>
