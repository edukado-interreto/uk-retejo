<template>
  <n-alert v-if="success" type="success" id="successAlert" :closable="false" style="margin-bottom: 2rem">
    <template v-if="edit">
      <p style="font-size: 1.1rem">Via mendo estis sukcese sendita al la Kongresa Fako.</p>
    </template>
    <template v-else>
      <p style="font-size: 1.1rem" v-if="sum > 0 && form.pagmaniero === 'Stripe'">
        Via pago ({{ sum }}&nbsp;€) sukcese efektiviĝis.
      </p>
      <p style="font-size: 1.1rem">Vi sukcese aliĝis al la 111-a Universala Kongreso de Esperanto.</p>
    </template>
    <p style="font-size: 1.1rem">
      Retmesaĝo kun pli detalaj informoj estis sendita al
      {{ formToSend.retadreso ? formToSend.retadreso : 'via retpoŝtadreso' }}.
    </p>
    <p style="text-align: center">
      <n-button @click="$router.go()" type="primary" size="large">{{
        edit ? 'Redakti la mendon' : 'Aligi plian personon'
      }}</n-button>
    </p>
  </n-alert>

  <n-form
    v-else
    @submit="submitForm($event)"
    label-placement="top"
    :model="form"
    ref="formRef"
    :rules="rules"
    class="mainform"
  >
    <n-alert type="error" id="errorAlert" v-if="hasErrors" :closable="false" style="margin-bottom: 2rem">
      Verŝajne iu(j) kampo(j) estis malĝuste plenigita(j). Bonvolu rekontroli la datumojn, kiujn vi entajpis.
    </n-alert>

    <n-h3>Personaj informoj</n-h3>

    <uea-code-input
      v-model="form.uea_kodo"
      field-name="uea_kodo"
      help="Se vi havas/memoras, nepre indiku por ne plenigi la sekvantan enketilon."
      @code-checked="ueaCodeResult"
    />

    <n-alert type="success" v-if="discount > 0" :closable="false" style="margin-top: 1rem; margin-bottom: 2rem">
      Pro via partopreno en UK 2025 vi ricevas {{ discount }}-eŭran rabaton.
    </n-alert>

    <slide-transition>
      <form-personal-data
        v-model="form"
        v-model:showPersonalData="showPersonalData"
        :missingFields="missingFields"
        :ueaCodeValid="ueaCodeValid"
      />
    </slide-transition>

    <n-h3>Nomŝildo</n-h3>

    <form-nametag v-model="form" />

    <n-h3>Kotizo</n-h3>

    <form-membership-price
      v-model="form"
      :errors="errors"
      :countryCategory="countryCategory"
      :requiredFields="requiredFields"
      :showPersonalData="showPersonalData"
      :pricesList="pricesList"
      :memberAgeGroup="memberAgeGroup"
      :detailed-sum="detailedSum"
      :special-category="specialCategory"
      :membership-locked="membershipLocked"
    />

    <n-h3>Komentoj</n-h3>
    <text-input v-model="form.komento" field-name="komento" type="textarea" autocapitalize="on" />

    <n-h3>Kondiĉoj</n-h3>

    <form-conditions v-model="form" />

    <div v-show="!edit && (sum === null || sum > 0)">
      <n-h3>Pagmaniero</n-h3>
      <p>
        <strong>Pagenda sumo: {{ sum }}&nbsp;€</strong>
      </p>
      <form-payment
        ref="payments"
        v-model="form"
        v-model:is-loading="isLoading"
        :form-to-send="formToSend"
        :ueaCodeValid="ueaCodeValid"
      />
    </div>

    <template v-if="edit">
      <n-h3 id="mendilo">Mendilo</n-h3>

      <form-booking
        v-model="form"
        :default-data="defaultData"
        :food-type-required="foodTypeRequired"
        :foodTypeCompanionRequired="foodTypeCompanionRequired"
      />
    </template>

    <n-form-item>
      <n-button @click="sendForm" size="large" type="primary" :loading="isLoading" :disabled="!canSubmit">
        {{ edit ? 'Konservi la mendon' : 'Mi aliĝas' }}
      </n-button>
    </n-form-item>
  </n-form>
</template>

<script>
import { defineAsyncComponent, h } from 'vue';
import { mapGetters } from 'vuex';
import { calculatePrice } from '@/helpers/price.js';
import TextInput from '@/components/form/fields/TextInput.vue';
import { useDialog, useMessage, NInput, NButton, NAlert } from 'naive-ui';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import UeaCodeInput from './form/fields/UeaCodeInput.vue';
import FormPersonalData from '@/components/form/parts/FormPersonalData.vue';
import FormNametag from '@/components/form/parts/FormNametag.vue';
import FormMembershipPrice from '@/components/form/parts/FormMembershipPrice.vue';
import FormConditions from '@/components/form/parts/FormConditions.vue';
import FormPayment from '@/components/form/parts/FormPayment.vue';
const FormBooking = defineAsyncComponent(() => import('@/components/form/parts/FormBooking.vue'));

export default {
  props: {
    defaultData: {
      type: Object,
      required: true,
    },
    edit: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  name: 'MainForm',
  components: {
    FormBooking,
    FormPayment,
    FormConditions,
    FormMembershipPrice,
    FormNametag,
    FormPersonalData,
    UeaCodeInput,
    SlideTransition,
    TextInput,
  },
  data() {
    return {
      message: useMessage(),
      dialog: useDialog(),
      form: {},
      ueaCodeValid: false,
      showPersonalData: true,
      missingFields: [], // When fetching a member by UEA code: empty fields
      memberAgeGroup: null,
      countryCategoryFromDB: null,
      discount: 0,
      specialCategory: null,

      membershipLocked: false,

      success: false,
      errors: { value: {} }, // Trick to make it reactive in provide/inject
      canSubmit: true,

      // For Stripe
      isLoading: false,

      renderErrorMessage: (props) => {
        const { type } = props;
        return h(
          NAlert,
          {
            closable: props.closable,
            onClose: props.onClose,
            type: type === 'loading' ? 'default' : type,
            title: 'Eraro',
            style: {
              boxShadow: 'var(--n-box-shadow)',
              maxWidth: 'calc((100vw - 32px) / 1.7)',
              transform: 'scale(1.7) translateY(30%)',
            },
          },
          {
            default: () => props.content,
          },
        );
      },
    };
  },
  computed: {
    ...mapGetters(['fields', 'countries', 'detectedCountry', 'formOptions', 'prices', 'currentPeriod']),
    requiredFields() {
      const fields = {};
      for (const field in this.fields) {
        fields[field] =
          'validation_rules' in this.fields[field] &&
          Object.values(this.fields[field].validation_rules).includes('required');
      }

      const required = {
        ...fields,
        lando: this.showPersonalData,
        familia_nomo: this.showPersonalData,
        retadreso: !this.ueaCodeValid || this.missingFields.includes('retadreso'),
        // TODO: bug ici ?
        naskigxdato:
          (this.showPersonalData || this.missingFields.includes('naskigxdato')) &&
          (this.form.kotizo === 'junulo' ||
            this.form.kotizo === 'infano' ||
            this.formToSend.volas_membrigxi === this.formOptions.boolValues.yes),
        adreso: this.showPersonalData && this.formToSend.membreco_tipo === 'MA',
        urbo: this.showPersonalData && this.formToSend.membreco_tipo === 'MA',
        posxtkodo: this.showPersonalData && this.formToSend.membreco_tipo === 'MA',
        cxefaligxinto: this.form.kotizo === 'kunulo' || this.form.kotizo === 'akompananto',
        handikapatestilo: this.form.kotizo === 'handikapulo',
        konsento_donaclisto: Object.keys(this.form).some((k) => k.startsWith('donaco_') && this.form[k] > 0),
        uea_kodo_paganto: !this.edit && this.sum > 0 && this.form.pagmaniero === 'UEA-alia',
        karto_posedanto: !this.edit && this.sum > 0 && this.form.pagmaniero === 'Stripe',
        karto_retadreso: !this.edit && this.sum > 0 && this.form.pagmaniero === 'Stripe',
        pagmaniero: !this.edit && this.sum > 0,

        volas_membrigxi: !this.edit && this.form.membreco === this.formOptions.boolValues.no,
        membreco_tipo: !this.edit && this.form.volas_membrigxi === this.formOptions.boolValues.yes,

        mangxotipo: this.edit && this.foodTypeRequired,
        mangxotipo_kunlogxanto: this.edit && this.foodTypeCompanionRequired,
        ak_cxambro: this.edit && this.form.ak,
        ak_kunlogxanto2:
          this.edit &&
          this.form.ak &&
          (this.akPeopleInRoom > 2 || (this.akPeopleInRoom == 2 && !this.form.ak_kunlogxanto)),
        pk_cxambro: this.edit && this.form.pk,
        pk_kunlogxanto2:
          this.edit &&
          this.form.pk &&
          (this.pkPeopleInRoom > 2 || (this.pkPeopleInRoom == 2 && !this.form.pk_kunlogxanto)),
        hotelo_cxambro: this.edit && this.form.hotelo,
        hotelo_alternativo: this.edit && this.form.hotelo,
        hotelo_de: this.edit && this.form.hotelo,
        hotelo_gxis: this.edit && this.form.hotelo,
        hotelo_kunlogxanto2:
          this.edit &&
          this.form.hotelo &&
          this.hotelPayForRoom &&
          (this.hotelPeopleInRoom > 2 || (this.hotelPeopleInRoom == 2 && !this.form.hotelo_kunlogxanto)),
      };

      // In edit mode: all non-editable fields are made non-mandatory to avoid potential bugs
      if (this.edit) {
        for (const [fieldname, fielddata] of Object.entries(this.fields)) {
          if (fielddata.editable === false) {
            required[fieldname] = false;
          }
        }
      }

      return required;
    },
    hasErrors() {
      return Object.keys(this.errors.value).length > 0;
    },
    hotelPeopleInRoom() {
      if (!this.form.hotelo || !this.form.hotelo_cxambro) {
        return 1;
      }
      return this.formOptions.hotels[this.form.hotelo].rooms[this.form.hotelo_cxambro].people;
    },
    hotelPayForRoom() {
      if (!this.form.hotelo) {
        return false;
      }
      return this.formOptions.hotels[this.form.hotelo].payForRoom;
    },
    akPeopleInRoom() {
      if (!this.form.ak || !this.form.ak_cxambro) {
        return 1;
      }
      return this.formOptions.preposttrips[this.form.ak].rooms[this.form.ak_cxambro].people;
    },
    pkPeopleInRoom() {
      if (!this.form.pk || !this.form.pk_cxambro) {
        return 1;
      }
      return this.formOptions.preposttrips[this.form.pk].rooms[this.form.pk_cxambro].people;
    },
    formToSend() {
      const formData = {
        ...this.form,
        kongreslibro_adreso: this.form.konsento_kongreslibro ? this.form.kongreslibro_adreso : null,
        volas_membrigxi: this.form.membreco === this.formOptions.boolValues.no ? this.form.volas_membrigxi : null,
        membreco_tipo:
          this.form.membreco === this.formOptions.boolValues.no &&
          this.form.volas_membrigxi === this.formOptions.boolValues.yes
            ? this.form.membreco_tipo
            : null,
        cxefaligxinto:
          this.form.kotizo === 'kunulo' || this.form.kotizo === 'akompananto' ? this.form.cxefaligxinto : null,
        handikapatestilo: this.form.kotizo === 'handikapulo' ? this.form.handikapatestilo : null,
        pagmaniero: this.sum > 0 ? this.form.pagmaniero : null,
        uea_kodo_paganto: this.sum > 0 && this.form.pagmaniero === 'UEA-alia' ? this.form.uea_kodo_paganto : null,
        karto_posedanto: this.sum > 0 && this.form.pagmaniero === 'Stripe' ? this.form.karto_posedanto : null,
        karto_retadreso: this.sum > 0 && this.form.pagmaniero === 'Stripe' ? this.form.karto_retadreso : null,
        sumo: this.sum,
      };

      // These data are known from the UEA code, don't send them
      if (!this.showPersonalData) {
        const personalFields = [
          'lando',
          'persona_nomo',
          'familia_nomo',
          'genro',
          'titolo',
          'naskigxdato',
          'retadreso',
          'adreso',
          'urbo',
          'posxtkodo',
          'telefono',
        ];
        const canBeSent = ['naskigxdato'];
        if (!this.ueaCodeValid || this.missingFields.includes('retadreso')) {
          // To avoid circular reference
          canBeSent.push('retadreso');
        }
        personalFields.forEach((field) => {
          if (!canBeSent.includes(field) || !this.missingFields.includes(field)) {
            delete formData[field];
          }
        });
      }

      if (this.edit) {
        if (this.form.bankedo !== this.formOptions.boolValues.yes) {
          formData.bankedo_tipo = '';
        }
        if (!this.foodTypeRequired) {
          formData.mangxotipo = '';
        }
        if (!this.foodTypeCompanionRequired) {
          formData.mangxotipo_kunlogxanto = '';
        }
        // ak_cxambro
        if (!this.form.ak) {
          formData.ak_cxambro = '';
        }
        if (this.akPeopleInRoom < 2) {
          formData.ak_kunlogxanto = '';
          formData.ak_kunlogxanto2 = '';
        }
        // pk_cxambro
        if (!this.form.pk) {
          formData.pk_cxambro = '';
        }
        if (this.pkPeopleInRoom < 2) {
          formData.pk_kunlogxanto = '';
          formData.pk_kunlogxanto2 = '';
        }
        if (!this.form.hotelo) {
          formData.hotelo_cxambro = '';
          formData.hotelo_alternativo = '';
          formData.hotelo_de = '';
          formData.hotelo_gxis = '';
        }
        if (this.hotelPeopleInRoom != 2) {
          formData.hotelo_kunlogxanto = '';
        }
        if (this.hotelPeopleInRoom == 1) {
          formData.hotelo_kunlogxanto2 = '';
        }
      }

      return formData;
    },
    rules() {
      const rules = {};

      for (const field in this.requiredFields) {
        if (!(field in this.fields)) {
          continue;
        }
        if (this.requiredFields[field]) {
          rules[field] = {
            required: true,
            message: 'Ĉi tiu kampo estas deviga.',
          };
        } else {
          rules[field] = {};
        }
        if (
          'validation_rules' in this.fields[field] &&
          Object.values(this.fields[field].validation_rules).includes('float')
        ) {
          rules[field].type = 'number';
        }
        if (
          'bool' in this.fields[field] &&
          this.fields[field].bool &&
          (!('filter_rules' in this.fields[field]) ||
            !Object.values(this.fields[field].filter_rules).includes('to_boolean'))
        ) {
          rules[field].type = 'boolean';
          if ('required' in rules[field] && rules[field].required) {
            // Rule for required booleans
            rules[field].validator = (rule, value) => value === true;
          }
        }
        if ('array' in this.fields[field] && this.fields[field].array) {
          rules[field].type = 'array';
        }
      }
      return rules;
    },
    countryCategory() {
      if (!this.showPersonalData && this.countryCategoryFromDB !== null) {
        return this.countryCategoryFromDB;
      }
      return this.countries[this.form.lando].category;
    },
    countryMembershipCategory() {
      if (!this.showPersonalData && this.countryMembershipCategoryFromDB !== null) {
        return this.countryMembershipCategoryFromDB;
      }
      return this.countries[this.form.lando].uea_cat;
    },
    pricesList() {
      const prices = {};
      const period = this.edit && 'aligxperiodo' in this.form ? this.form.aligxperiodo : this.currentPeriod;
      for (const key in this.prices.participation) {
        const membershipIndex =
          this.form.membreco === this.formOptions.boolValues.yes ||
          this.form.volas_membrigxi === this.formOptions.boolValues.yes
            ? 0
            : 1;
        prices[key] = {
          ...this.prices.participation[key],
          price: this.prices.participation[key].price[membershipIndex][period][this.countryCategory],
          priceM: this.prices.participation[key].price[0][period][this.countryCategory],
          priceNM: this.prices.participation[key].price[1][period][this.countryCategory],
        };
      }
      return prices;
    },
    detailedSum() {
      return calculatePrice(
        this.form,
        this.pricesList,
        this.countryMembershipCategory,
        this.discount,
        this.formOptions,
        this.showPersonalData,
        this.memberAgeGroup,
      );
    },
    sum() {
      if (this.form.kotizo === null) {
        return null;
      }
      return this.detailedSum.sum;
    },
    foodTypeRequired() {
      if (this.form.ak || this.form.pk) {
        return true;
      }
      for (const trip of this.form.ekskursoj) {
        if (trip.startsWith('E')) {
          return true;
        }
      }
      return false;
    },
    foodTypeCompanionRequired() {
      return (
        (this.akPeopleInRoom > 1 && !this.form.ak_cxefmendanto) ||
        (this.pkPeopleInRoom > 1 && !this.form.pk_cxefmendanto)
      );
    },
  },
  methods: {
    submitForm(event) {
      event.preventDefault();
    },
    updateNameTagCountry(value) {
      if (value in this.countries) {
        this.form.sxildolando = this.countries[value].name;
      }
    },
    ueaCodeResult(data) {
      this.showPersonalData = !data.valid;
      this.ueaCodeValid = data.valid;
      if ('member' in data) {
        this.missingFields = data.member.missingFields;
        if (this.missingFields.includes('retadreso')) {
          this.showPersonalData = true;
        }
        this.memberAgeGroup = data.member.ageGroup;
        this.countryCategoryFromDB = data.member.countryCategory;
        this.countryMembershipCategoryFromDB = data.member.countryMembershipCategory;
        this.form.membreco = data.member.isMember ? this.formOptions.boolValues.yes : this.formOptions.boolValues.no;
        this.membershipLocked = true;
        this.discount = data.member.discount;
        this.specialCategory = data.member.specialCategory;
        if (this.specialCategory in this.pricesList) {
          this.form.kotizo = this.specialCategory;
        }

        if (data.member.isRegistered) {
          this.dialog.warning({
            title: 'Vi jam aliĝis',
            content:
              'Vi jam aliĝis al la 111-a UK. Se vi volas ŝanĝi ion en via mendo, ne plenigu la aliĝilon denove, sed kontaktu kongresoj@co.uea.org.',
            positiveText: 'Mi komprenis',
          });
        }
      } else {
        this.missingFields = [];
        this.memberAgeGroup = null;
        this.countryCategoryFromDB = null;
        this.specialCategory = null;
        this.discount = 0;
        this.membershipLocked = false;
      }
    },
    sendForm(e) {
      e.preventDefault();
      this.$refs.formRef
        .validate((errors) => {
          if (!errors) {
            this.signup(!this.edit && this.form.pagmaniero === 'Stripe');
          }
        })
        .catch((errors) => {
          errors.forEach((err) => {
            this.errors.value[err[0].field] = err[0].message;
          });
          this.scrollTo(errors[0][0].field);
          this.message.error('Kontrolu, ĉu vi plenigis ĉiujn necesajn kampojn.', {
            keepAliveOnHover: true,
            render: this.renderErrorMessage,
            duration: 5000,
          });
        });
    },
    async signup(pay = false) {
      try {
        const d = await (pay
          ? this.$refs.payments.$refs.Stripable.signup_pay()
          : this.$refs.payments.$refs.Stripable.signup());
        console.log(d);
        if (d.success) {
          this.success = true;
          this.scrollTo('success');
        }
      } catch (e) {
        console.log(e);
        try {
          this.errors.value = JSON.parse(e.error_msg);
          this.message.error('Kontrolu, ĉu vi bone plenigis ĉiujn kampojn.', {
            keepAliveOnHover: true,
          });
          this.scrollTo('errorAlert');
        } catch (err) {
          this.canSubmit = false; // To avoid registering or paying twice
          this.showErrorMessage(JSON.stringify(e));
          console.log(err);
        }
      }
    },
    showErrorMessage(msg) {
      this.dialog.error({
        title: 'Eraro',
        content: () => [
          h('p', [
            'Okazis eraro. Bonvolu ne provi aliĝi denove, sed kontakti ',
            h('a', { href: 'mailto:kongresoj@co.uea.org' }, 'kongresoj@co.uea.org'),
            '.',
          ]),
          h('p', 'Bonvolu inkluzivi la jenan erarmesaĝon por helpi al ni solvi la problemon:'),
          h(NInput, { type: 'textarea', disabled: true, value: msg }),
        ],
        action: () => [
          h(
            NButton,
            {
              onClick: () => {
                navigator.clipboard.writeText(msg);
                this.message.success('La erarmesaĝo estis kopiita al la tondujo.', { keepAliveOnHover: true });
              },
              size: 'small',
            },
            'Kopii la tekston',
          ),
          h(NButton, { onClick: () => this.dialog.destroyAll(), size: 'small', type: 'error' }, 'Fermi'),
        ],
      });
    },
  },
  created() {
    this.$store.dispatch('setEditMode', this.edit);
    if (this.edit) {
      this.form = JSON.parse(JSON.stringify(this.defaultData)); // Dumb method to create a deep copy of the object
    } else {
      this.form = this.defaultData;
    }
    if (this.form.lando === null) {
      this.form.lando = this.detectedCountry;
      this.updateNameTagCountry(this.detectedCountry);
    }
  },
  provide() {
    return {
      formErrors: this.errors,
    };
  },
};
</script>

<style lang="scss">
form.mainform {
  padding-left: 1rem;
  border-left: 1px solid #25aae1;

  @media screen and (max-width: 1024px) {
    padding-left: 0;
    border-left: none;
  }

  h2 {
    font-size: 1.7rem;
    text-align: center;
  }

  h3,
  h4 {
    color: #3366ff;
    background: #ccffcc;
    margin: 2rem 0 2.6rem;
  }

  h3 {
    padding: 5px 8px;
    font-size: 1.3rem;
  }

  h4 {
    padding: 3px 8px;
    font-size: 1.1rem;
    margin-top: 1rem;
  }

  h3 + h4 {
    margin-top: 0;
  }

  a {
    text-decoration: none;
    color: #0030db;
  }

  a:hover,
  a:active,
  a:focus {
    text-decoration: underline;
    color: #3366ff;
  }
}
</style>
