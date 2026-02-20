<template>
  <n-card v-if="showPersonalData" class="custom-card" title="Personaj informoj pri la aliĝanto">
    <n-alert v-if="missingFields.includes('retadreso')" type="warning" :closable="false" style="margin-bottom: 2rem">
      Ni trovis, ke la datumoj ligitaj kun tiu ĉi UEA-kodo ne estas kompletaj, pro tio ni petas vin plenigi ĉiujn
      datumojn.
    </n-alert>
    <select-input
      v-model="form.lando"
      field-name="lando"
      :options="countryOptions"
      placeholder="Elektu landon"
      filterable
      width="20em"
      @update:modelValue="updateNameTagCountry"
    />
    <text-input
      v-model="form.persona_nomo"
      field-name="persona_nomo"
      @input="updateNametagName"
      autocapitalize="words"
    />
    <text-input
      v-model="form.familia_nomo"
      field-name="familia_nomo"
      @input="updateNametagName"
      autocapitalize="words"
    />

    <n-grid x-gap="12" cols="1 s:2" responsive="screen">
      <n-gi>
        <radio-input v-model="form.genro" field-name="genro" :options="formOptions.genders" />
      </n-gi>
      <n-gi>
        <select-input v-model="form.titolo" field-name="titolo" :options="formOptions.titles" clearable width="12em" />
      </n-gi>
      <n-gi>
        <date-input v-model="form.naskigxdato" field-name="naskigxdato" max="now" @update:modelValue="checkBirthDate" />
      </n-gi>
      <n-gi>
        <text-input
          v-if="!ueaCodeValid || missingFields.includes('retadreso')"
          v-model="form.retadreso"
          field-name="retadreso"
          type="email"
          @input="form.karto_retadreso = form.retadreso"
        />
        <n-p v-else-if="ueaCodeValid"><br />Via retpoŝtadreso jam estas konata.</n-p>
      </n-gi>
      <n-gi :span="2">
        <text-input v-model="form.adreso" field-name="adreso" autocapitalize="on" />
      </n-gi>
      <n-gi>
        <text-input v-model="form.urbo" field-name="urbo" autocapitalize="on" />
      </n-gi>
      <n-gi>
        <text-input v-model="form.posxtkodo" field-name="posxtkodo" />
      </n-gi>
      <n-gi>
        <text-input v-model="form.telefono" field-name="telefono" type="tel" />
      </n-gi>
    </n-grid>
  </n-card>
  <n-card v-else class="custom-card">
    <p>
      Viaj personaj informoj estas konataj de UEA kaj tial vi ne bezonas resendi ilin. Se vi opinias, ke iuj informoj
      bezonas esti korektitaj, bonvolu remalfermi la enketilon.
    </p>
    <div style="text-align: center">
      <n-button @click="$emit('update:showPersonalData', true)" type="primary"
        >Redakti miajn personajn informojn</n-button
      >
    </div>

    <template v-if="missingFields.includes('naskigxdato') || missingFields.includes('retadreso')">
      <p style="margin-top: 2rem">La jenaj informoj ne estas konataj de UEA, bonvolu plenigi ilin.</p>
      <n-grid x-gap="12" cols="1 s:2" responsive="screen">
        <n-gi v-if="missingFields.includes('retadreso')">
          <text-input
            v-model="form.retadreso"
            field-name="retadreso"
            type="email"
            @input="form.karto_retadreso = form.email"
          />
        </n-gi>
        <n-gi v-if="missingFields.includes('naskigxdato')">
          <date-input
            v-model="form.naskigxdato"
            field-name="naskigxdato"
            max="now"
            @update:modelValue="checkBirthDate"
          />
        </n-gi>
      </n-grid>
    </template>
  </n-card>
</template>

<script>
import SelectInput from '@/components/form/fields/SelectInput.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import DateInput from '@/components/form/fields/DateInput.vue';
import { mapGetters } from 'vuex';
import { useDialog } from 'naive-ui';

export default {
  components: { DateInput, RadioInput, TextInput, SelectInput },
  props: {
    modelValue: Object,
    showPersonalData: Boolean,
    missingFields: Object,
    ueaCodeValid: Boolean,
  },
  emits: ['update:modelValue', 'update:showPersonalData'],
  name: 'FormPersonalData',
  data() {
    return {
      dialog: useDialog(),
    };
  },
  computed: {
    ...mapGetters(['countries', 'formOptions']),
    form: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
    countryOptions() {
      return Object.keys(this.countries).map((key) => {
        return { value: key, label: this.flagEmoji(key) + ' ' + this.countries[key].name };
      });
    },
  },
  methods: {
    updateNametagName() {
      if (this.form.persona_nomo.trim() === '') {
        this.form.sxildonomo = this.form.familia_nomo.trim();
      } else {
        this.form.sxildonomo = this.form.persona_nomo.trim();
      }
      this.form.karto_posedanto = this.form.sxildonomo;
    },
    updateNameTagCountry(value) {
      this.$store.dispatch('setUserCountry', value); // Special offer for Czechs
      if (value in this.countries) {
        this.form.sxildolando = this.countries[value].name;
      }
    },
    checkBirthDate(date) {
      const year = date.split('-')[0];
      if (parseInt(year) >= 2025) {
        this.dialog.warning({
          title: `Naskiĝdato en ${year}`,
          content: `Vi indikis kiel naskiĝdaton la ${this.formatDate(date, true, true)}. Ĉu vi aligas bebon? Se ne, bonvolu kontroli la naskiĝdaton.`,
          positiveText: 'Fermi',
        });
      }
    },
  },
};
</script>

<style scoped></style>
