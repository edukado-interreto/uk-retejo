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
              :disabled="form.naskigxdato"
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

<script>
import { NFormItemGi } from 'naive-ui';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import SelectInput from '@/components/form/fields/SelectInput.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import { mapGetters } from 'vuex';
import axios from 'axios';
import download from 'downloadjs';
import { flagEmoji } from '@/helpers/functions';

export default {
  name: 'FormInvitation',
  components: { SlideTransition, SelectInput, TextInput, NFormItemGi },
  props: {
    modelValue: Object,
  },
  emits: ['update:modelValue'],
  data() {
    return {
      invitationNeeded: false,
      passportValidFrom: null,
      passportValidTo: null,
      birthDate: null,
      loading: false,
      defaultName: null,
    };
  },
  computed: {
    ...mapGetters(['countries']),
    countryOptions() {
      return Object.keys(this.countries).map((key) => {
        return { value: key, label: flagEmoji(key) + ' ' + this.countries[key].name };
      });
    },
    canSubmit() {
      return (
        this.form.pasporto && this.passportValidFrom && this.passportValidTo && this.birthDate && this.form.sxtataneco
      );
    },
    form: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
  methods: {
    download() {
      this.loading = true;
      axios
        .post(
          '/invitation',
          {
            id: this.$route.params.id,
            passportNumber: this.form.pasporto,
            passportValidFrom: this.passportValidFrom,
            passportValidTo: this.passportValidTo,
            birthDate: this.birthDate,
            country: this.form.sxtataneco,
          },
          { responseType: 'blob' },
        )
        .then((response) => {
          download(response.data, `Invitletero ${this.defaultName}.pdf`);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    if (!this.form.sxtataneco) {
      this.form.sxtataneco = this.form.lando;
    }
    if (this.form.naskigxdato) {
      this.birthDate = this.form.naskigxdato;
    }
    this.defaultName = (this.form.persona_nomo + ' ' + this.form.familia_nomo).trim();
  },
};
</script>

<style scoped></style>
