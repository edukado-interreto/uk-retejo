<template>
  <n-h1>Pago par bankokarto</n-h1>
  <n-alert v-if="error !== undefined" :title="errorTitle" type="error">
    {{ error }}
  </n-alert>

  <loading-spinner v-if="loading" />
  <n-alert
      v-else-if="success"
      type="success"
      id="successAlert"
      :closable="false"
  >
    <p style="font-size: 1.1rem;">Vi sukcese pagis {{ userData.sum }}&nbsp;€. Vi baldaŭ ricevos retpoŝtan konfirmon.</p>
  </n-alert>
  <template v-else-if="error === undefined">
    <ul>
      <li>Nomo: {{ userData.name }}</li>
      <li>Kongresa numero: {{ userData.kn }}</li>
      <li>Pagenda sumo: <strong style="font-size: 1.3em;">{{ userData.sum }}&nbsp;€</strong> (5%-a ĝirkosto estis aldonita)</li>
    </ul>

    <n-card title="Pagformularo" class="custom-card">
      <stripable-formdict
          ref="Stripable"
          :formdict="formToSend"
          :stripe_key="stripe.publishableKey"
          :card_owner_fullname="cardOwner"
          :card_owner_email="cardEmail"
          :server_endpoint="server_endpoint"
          :please_wait="paymentLoading"
          @wait_start="paymentLoading = true"
          @wait_end="paymentLoading = false"
          @card_change="on_card_change"
      />
      <div style="color: #d03050; padding-top: 2px;">{{ card_errors }}</div>
      <n-grid x-gap="12" :cols="2" style="margin-top: 1.5rem;">
        <n-gi>
          <n-form-item
              label="Retadreso de la posedanto"
          >
            <n-input
                v-model:value="cardEmail"
            />
          </n-form-item>
        </n-gi>
        <n-gi>
          <n-form-item
              label="Nomo de la posedanto"
          >
            <n-input
                v-model:value="cardOwner"
            />
          </n-form-item>
        </n-gi>
      </n-grid>
      <p>Pagformularo provizita de <a href="https://stripe.com/" target="_blank">Stripe</a>. Kartdatumoj ne estas iel ajn konservataj de nia sistemo, nek videblas al ni.</p>

      <n-button
          @click="signup"
          size="large"
          type="primary"
          :loading="paymentLoading"
      >
        Pagi
      </n-button>
    </n-card>
  </template>
</template>

<script>
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import axios from "axios";
import {useMessage} from "naive-ui";
import StripableFormdict from "@/components/form/fields/StripableFormdict.vue";

export default {
  name: "CardPayment",
  components: {StripableFormdict, LoadingSpinner},
  data() {
    return {
      loading: true,
      uniqueId: undefined,
      errorTitle: undefined,
      error: undefined,
      userData: [],
      message: useMessage(),

      success: false,
      paymentLoading: false,
      cardOwner: '',
      cardEmail: '',
      card_errors: undefined,
      server_endpoint: axios.defaults.baseURL + '/directpayment',
      stripe: {
        publishableKey: import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY
      }
    };
  },
  computed: {
    formToSend() {
      return {
        id: this.uniqueId,
        sum: this.userData.sum,
        direct_payment: true,
        persona_nomo: this.userData.persona_nomo,
        familia_nomo: this.userData.familia_nomo,
      }
    }
  },
  methods: {
    fetchData() {
      axios.post('/getsumtopay', { id: this.uniqueId })
          .then(result => {
            if (result.data.success) {
              this.userData = result.data.userData;
              this.cardOwner = this.userData.name;
              this.cardEmail = this.userData.email;
            }
            else {
              this.error = result.data.error;
              this.errorTitle = result.data.errorTitle;
            }
          })
          .catch((error) => {
            this.message.error(error, {
              keepAliveOnHover: true
            });
          })
          .finally(() => {
            this.loading = false;
          });
    },
    on_card_change(d) {
      console.log('on_card_change:', d);
      this.card_errors = (d.error) ? d.error.message : '';
    },
    async signup() {
      try {
        const d = await this.$refs.Stripable.signup_pay();
        console.log(d);
        if (d.success) {
          this.success = true;
        }
      } catch(e) {
        console.log(e);
        try {
          this.errors.value = JSON.parse(e.error_msg);
          this.message.error("Kontrolu, ĉu vi bone plenigis ĉiujn kampojn.", {
            keepAliveOnHover: true
          });
          this.scrollTo('errorAlert');
        }
        catch (err) {
          this.dialog.error({
            title: "Eraro",
            content: "Okazis eraro.",
            positiveText: "Fermi",
          });
          console.log(err);
        }
      }
    },
  },
  created() {
    this.uniqueId = this.$route.params.id;
    if (this.uniqueId === undefined) {
      this.errorTitle = 'Mankanta identigilo';
      this.error = 'Se vi volas mendi servojn, bonvolu uzi la ligilon, kiu estis sendita al vi per retpoŝto.';
      this.loading = false;
    }
    else {
      this.fetchData();
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
  color: #0030DB;
}

a:hover, a:active, a:focus {
  text-decoration: underline;
  color: #3366FF;
}
</style>