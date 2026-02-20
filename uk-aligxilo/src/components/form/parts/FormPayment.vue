<template>
  <radio-input
      v-if="!editMode"
      v-model="form.pagmaniero"
      field-name="pagmaniero"
      :options="pagmanieroj"
      vertical
  />

  <slide-transition>
    <uea-code-input
        v-if="form.pagmaniero === 'UEA-alia'"
        v-model="form.uea_kodo_paganto"
        field-name="uea_kodo_paganto"
        help="La kontposedanto nepre rajtigu skribe UEA pri la pago!"
    />
  </slide-transition>
  <slide-transition>
    <n-p v-if="form.pagmaniero !== null && form.pagmaniero.startsWith('Peranto:')">Bazaj informoj pri via aliĝo estos senditaj ankaŭ al la peranto.</n-p>
  </slide-transition>
  <slide-transition>
    <n-card title="Pagformularo" class="custom-card" v-show="form.pagmaniero === 'Stripe'">
      <stripable-formdict
          ref="Stripable"
          :formdict="formToSend"
          :stripe_key="stripe.publishableKey"
          :card_owner_fullname="form.karto_posedanto"
          :card_owner_email="form.karto_retadreso"
          :server_endpoint="server_endpoint"
          :please_wait="isLoading"
          @wait_start="$emit('update:isLoading', true)"
          @wait_end="$emit('update:isLoading', false)"
          @card_change="on_card_change"
      />
      <div style="color: #d03050; padding-top: 2px;">{{ card_errors }}</div>
      <n-grid x-gap="12" :cols="2" style="margin-top: 1.5rem;">
        <n-gi>
          <text-input
              v-model="form.karto_retadreso"
              field-name="karto_retadreso"
              type="email"
          />
        </n-gi>
        <n-gi>
          <text-input
              v-model="form.karto_posedanto"
              field-name="karto_posedanto"
          />
        </n-gi>
      </n-grid>
      <p>Pagformularo provizita de <a href="https://stripe.com/" target="_blank">Stripe</a>. Kartdatumoj ne estas iel ajn konservataj de nia sistemo, nek videblas al ni.</p>
    </n-card>
  </slide-transition>
</template>

<script>
import {mapGetters} from "vuex";
import RadioInput from "@/components/form/fields/RadioInput.vue";
import SlideTransition from "@/components/ui/SlideTransition.vue";
import UeaCodeInput from "@/components/form/fields/UeaCodeInput.vue";
import StripableFormdict from "@/components/form/fields/StripableFormdict.vue";
import TextInput from "@/components/form/fields/TextInput.vue";
import axios from "axios";

export default {
  components: {TextInput, StripableFormdict, UeaCodeInput, SlideTransition, RadioInput},
  props: {
    modelValue: Object,
    isLoading: Boolean,
    formToSend: Object,
    ueaCodeValid: Boolean,
  },
  emits: ['update:modelValue', 'update:isLoading'],
  name: "FormPayment",
  data() {
    return {
      card_errors: undefined,
      server_endpoint: axios.defaults.baseURL + '/saveform',
      stripe: {
        publishableKey: import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY
      }
    }
  },
  computed: {
    ...mapGetters([
      'countries',
      'formOptions',
      'editMode'
    ]),
    form: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    },
    pagmanieroj() {
      const payments = { ...this.formOptions.payment };
      payments.Stripe += ' — Ni rekomendas uzi tiun ĉi pagmanieron ĉar tio ebligos al UEA plej rapide trakti la aliĝon.';

      if (this.form.lando in this.formOptions.perantoj) {
        // Turn object into array
        const options = [];
        for (const key in payments) {
          if (!(!this.ueaCodeValid && key === 'UEA')) {
            options.push({
              value: key,
              label: payments[key]
            });
          }
        }
        // Insert perantoj
        this.formOptions.perantoj[this.form.lando].forEach(peranto => {
          options.splice(-2, 0, {
            value: "Peranto: " + peranto.uea_kodo,
            label: "Pere de kongresa peranto en " + this.countries[this.form.lando].name + ": " + peranto.nomo
          });
        });
        // Return array as object
        const optionsObject = {};
        options.forEach(peranto => {
          optionsObject[peranto.value] = peranto.label;
        });
        return optionsObject;
      }
      return payments;
    },
  },
  methods: {
    on_card_change(d) {
      console.log('on_card_change:', d);
      this.card_errors = (d.error) ? d.error.message : '';
    },
  }
}
</script>

<style scoped>

</style>