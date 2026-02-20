<template>
  <div>
    <div ref="card_element" id="card_element"></div>
  </div>
</template>

<script>
import { loadStripe } from '@stripe/stripe-js';

export default {
  name: 'StripableFormdict',
  props: [
    'formdict',
    'stripe_key',
    'card_owner_fullname',
    'card_owner_email',
    'server_endpoint',
    'please_wait',
  ],
  data() {
    return {
      stripe: undefined,
      elements: undefined,
      card_element: undefined
    };
  },
  mounted() {
    this.stripe_init();
  },
  methods: {
    stripe_init() {
      loadStripe(this.stripe_key)
          .then(result => {
            this.stripe = result;
            this.elements = this.stripe.elements();
            this.card_element = this.elements.create('card');
            this.card_element.mount('#card_element');

            this.card_element.addEventListener('change', d => {
              this.$emit('card_change', d);
            });
          });
    },
    async calculate_price() {

      if (this.please_wait) return;

      this.$emit('wait_start');

      let ret;

      try {
        ret = await (await fetch(
            this.server_endpoint,
            {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify({
                'op': 'calculate-price',
                'formdict': this.formdict
              })
            }
        )).json();

      } catch(e) {

        this._ajax_error_hdl(e);

      } finally {

        this.$emit('wait_end');

      }

      if (typeof ret === 'object' && 'error_code' in ret) {
        this._ajax_error_hdl(ret);
        return;
      }

      return ret;

    },
    async signup() {

      if (this.please_wait) return;

      this.$emit('wait_start');

      let retText, retJson;

      try {
        retText = await (await fetch(
            this.server_endpoint,
            {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify({
                'op': 'direct-process',
                'formdict': this.formdict
              })
            }
        )).text();
      } catch(e) {
        this._ajax_error_hdl(e);
      } finally {
        this.$emit('wait_end');
      }

      try {
        retJson = JSON.parse(retText);
      } catch(e) {
        this._ajax_error_hdl(e, retText);
      }

      if (typeof retJson === 'object' && 'error_code' in retJson) {
        this._ajax_error_hdl(retJson);
        return;
      }

      return retJson;

    },
    async signup_pay() {

      if (this.please_wait) return;

      this.$emit('wait_start');

      let retText, retJson;

      try {
        // calculate the price from formdict (server-side),
        // get a client secret for the resulting amount
        retText = await (await fetch(
            this.server_endpoint,
            {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify({
                'op': 'pre-payment',
                'formdict': this.formdict
              })
            }
        )).text();
      } catch(e) {
        this._ajax_error_hdl(e);
      } finally {
        this.$emit('wait_end');
      }

      try {
        retJson = JSON.parse(retText);
      } catch(e) {
        this._ajax_error_hdl(e, retText);
      }

      if (typeof retJson === 'object' && 'error_code' in retJson) {
        this._ajax_error_hdl(retJson);
        return;
      }

      let stripe_ret;

      try {
        // get a PaymentIntent using the client secret
        stripe_ret = await this.stripe.handleCardPayment(
            retJson.client_secret,
            this.card_element,
            {
              payment_method_data: {
                billing_details: {
                  name: this.card_owner_fullname,
                  email: this.card_owner_email
                }
              }
            }
        );
      } catch(e) {
        this.$emit('wait_end');
        throw {
          'error_code': 'ERR_STRIPE_FATAL',
          'error_msg': 'Error while calling Stripe service',
          'original_error': e
        }
      }

      if (stripe_ret.error) {
        this.$emit('wait_end');
        throw {
          'error_code': 'ERR_STRIPE',
          'error_msg': stripe_ret.error.message,
          'original_error': stripe_ret.error
        };
      }

      let ret;

      try {
        // call the post-payment operation
        // with the PaymentIntent and the original formdict.
        // The server will check if the payment belongs
        // to the given formdict and in that case will
        // process the sign-up
        ret = await (await fetch(
            this.server_endpoint,
            {
              method: 'POST',
              mode: 'cors',
              body: JSON.stringify({
                'op': 'post-payment',
                'formdict': this.formdict,
                'intent': stripe_ret.paymentIntent.id
              })
            }
        )).json();

      } catch(e) {
        this.$emit('wait_end');
        this._ajax_error_hdl(e);
        return;
      }
      if (typeof ret === 'object' && 'error_code' in ret) {
        this.$emit('wait_end');
        this._ajax_error_hdl(ret);
        return;
      }

      this.$emit('wait_end');
      return ret;

    },
    _ajax_error_hdl(e, text = null) {
      if (('error_code' in e) && ('error_msg' in e)) {
        throw { // server-side application error
          'error_code': e.error_code,
          'error_msg': e.error_msg,
          'original_error': e,
          'server_response': text
        }
      }
      throw {
        'error_code': 'ERR_NETWORK',
        'error_msg': 'An error occurred while calling the remote service',
        'original_error': e,
        'server_response': text
      }
    },
  }
}
</script>

<style>
.StripeElement {
  background: white;
  color: rgba(255, 255, 255, 1);
  font-size: 14px;
  border-radius: 3px;
  height: 34px;
  box-sizing: border-box;
  padding-left: 12px;
  padding-right: 12px;
  padding-top: 8px;
  color: rgb(51, 54, 57);
  caret-color: #3366FF;
  border: 1px solid rgb(224, 224, 230);
  transition: -webkit-text-fill-color .3s cubic-bezier(.4, 0, .2, 1), caret-color .3s cubic-bezier(.4, 0, .2, 1), color .3s cubic-bezier(.4, 0, .2, 1), text-decoration-color .3s cubic-bezier(.4, 0, .2, 1)
}

.StripeElement:hover, .StripeElement:focus {
  border-color: #36ad6a;
}

.StripeElement.StripeElement--invalid {
  border-color: #d03050;
  caret-color: #d03050;
}

.StripeElement.StripeElement--invalid:hover, .StripeElement.StripeElement--invalid:focus {
  border-color: #de576d;
}
</style>