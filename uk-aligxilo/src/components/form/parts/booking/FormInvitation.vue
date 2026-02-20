<template>
  <div style="margin-bottom: 2.5rem">
    <n-form-item
        label-placement="left"
        :show-feedback="false"
    >
      <n-checkbox
          v-model:checked="invitationNeeded"
          id="invitationNeeded"
      >
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
              <n-input
                  id="invitationName"
                  :value="defaultName"
                  disabled
              />
            </n-form-item-gi>
            <n-form-item-gi
                label="Pasporta numero"
                :show-feedback="false"
            >
              <n-input
                  id="invitationName"
                  v-model:value="passportNumber"
              />
            </n-form-item-gi>

            <n-form-item-gi
                label="La pasporto validas ekde"
                :show-feedback="false"
            >
              <n-date-picker
                  v-model:formatted-value="passportValidFrom"
                  id="passportValidFrom"
                  type="date"
                  value-format="yyyy-MM-dd"
              />
            </n-form-item-gi>
            <n-form-item-gi
                label="La pasporto validas ĝis"
                :show-feedback="false"
            >
              <n-date-picker
                  v-model:formatted-value="passportValidTo"
                  id="passportValidTo"
                  type="date"
                  value-format="yyyy-MM-dd"
              />
            </n-form-item-gi>
            <n-form-item-gi
                label="Naskiĝdato"
                :show-feedback="false"
            >
              <n-date-picker
                  v-model:formatted-value="birthDate"
                  id="birthDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  :disabled="defaultBirthdate"
              />
            </n-form-item-gi>
            <n-form-item-gi
                label="Civitaneco"
                feedback="Bonvolu kontroli kaj korekti, se la loĝlando ne kongruas kun la civitaneco indikita en la pasporto."
            >
              <n-select
                  v-model:value="country"
                  id="invitation_country"
                  :options="countryOptions"
                  filterable
              />
            </n-form-item-gi>
        </n-grid>
        <div style="text-align: center; padding-top: 2rem;">
          <n-button
              type="info"
              @click="download"
              :disabled="!canSubmit"
              :loading="loading"
          >
            Elŝuti la invitilon
          </n-button>
        </div>
      </n-card>
    </slide-transition>
  </div>
</template>

<script>
import { NFormItemGi } from "naive-ui";
import SlideTransition from "@/components/ui/SlideTransition.vue";
import {mapGetters} from "vuex";
import axios from "axios";
import download from 'downloadjs';

export default {
  name: "FormInvitation",
  components: {SlideTransition, NFormItemGi},
  props: {
    defaultCountry: {
      type: String,
      default: null
    },
    defaultName: {
      type: String,
      default: null
    },
    defaultBirthdate: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      invitationNeeded: false,
      passportNumber: "",
      passportValidFrom: null,
      passportValidTo: null,
      birthDate: null,
      country: "",
      loading: false,
    }
  },
  computed: {
    ...mapGetters([
      'countries'
    ]),
    countryOptions() {
      return Object.keys(this.countries).map((key) => {
        return {value: key, label: this.flagEmoji(key) + " " + this.countries[key].name};
      });
    },
    canSubmit() {
      return this.passportNumber && this.passportValidFrom && this.passportValidTo && this.birthDate && this.country;
    }
  },
  methods: {
    download() {
      this.loading = true;
      axios.post(
          '/invitation',
          {
            id: this.$route.params.id,
            passportNumber: this.passportNumber,
            passportValidFrom: this.passportValidFrom,
            passportValidTo: this.passportValidTo,
            birthDate: this.birthDate,
            country: this.country
          },
          {responseType: 'blob'}
      ).then((response) => {
        download(response.data, `Invitletero ${this.defaultName}.pdf`);
      }).finally(() => {
        this.loading = false;
      });
    }
  },
  created() {
    this.country = this.defaultCountry;
    if (this.defaultBirthdate) {
      this.birthDate = this.defaultBirthdate;
    }
  }
}
</script>

<style scoped>

</style>