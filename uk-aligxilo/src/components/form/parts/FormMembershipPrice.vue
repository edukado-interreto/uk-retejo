<template>
  <p>
    <router-link :to="{ name: 'pricetable' }" target="_blank" style="font-size: 1.2em">
      Vidi klarigojn pri la kotizoj
    </router-link>
  </p>
  <n-card class="custom-card" title="Membreco">
    <n-grid x-gap="28" cols="1 s:6 m:7" responsive="screen">
      <n-gi span="1 s:5 m:6">
        <select-input
          v-model="form.membreco"
          field-name="membreco"
          :options="formOptions.membership"
          width="38em"
          :disabled="membershipLocked"
          :help="membercoHelp"
          :style="{ 'margin-bottom': membershipLocked ? '1.5em' : null }"
        />
        <slide-transition>
          <div v-if="form.membreco !== formOptions.boolValues.yes">
            <select-input
              v-model="form.volas_membrigxi"
              field-name="volas_membrigxi"
              :options="membrigxo_options"
              width="38em"
              :label="
                membershipLocked
                  ? 'Laŭ niaj datumoj vi ne estas membro de UEA. Ĉu vi ŝatus remembriĝi kaj ĝui rabaton?'
                  : null
              "
            />

            <slide-transition>
              <div v-if="form.volas_membrigxi === formOptions.boolValues.yes">
                <select-input
                  v-model="form.membreco_tipo"
                  field-name="membreco_tipo"
                  :options="formOptions.membershipTypes"
                  width="16em"
                />
                <n-alert type="warning" v-if="!editMode">
                  Kontrolu, ĉu vi enskribis ĉiujn necesajn personajn datumojn supre.
                </n-alert>
              </div>
            </slide-transition>
            <p>
              Detaloj pri kotizoj kaj tipoj de membreco estas disponeblaj
              <a href="https://uea.org/alighoj/alighilo" target="_blank">en la retejo de UEA</a>.
            </p>
          </div>
        </slide-transition>
      </n-gi>
      <n-gi span="0 s:1">
        <img src="/img/uea.png" alt="UEA" style="margin-top: -40px" />
      </n-gi>
    </n-grid>
  </n-card>

  <price-type-choice
    v-model="form.kotizo"
    v-model:cxefaligxinto="form.cxefaligxinto"
    v-model:handikapatestilo="form.handikapatestilo"
    :required="requiredFields.kotizo"
    :show-birth-date-warning="showPersonalData"
    :prices-list="pricesList"
    :member-age-group="memberAgeGroup"
    :birthday="form.naskigxdato"
    :membership="showAsMember"
    :uea_kodo="form.uea_kodo"
    :full-name="(form.persona_nomo + ' ' + form.familia_nomo).trim()"
    field-name="kotizo"
    :special-category="specialCategory"
  />

  <n-card class="custom-card" title="Donacoj al kongresaj fondaĵoj" v-if="Object.keys(filteredFoundations).length > 0">
    <n-p>Mi donacas:</n-p>
    <n-grid x-gap="16" y-gap="16" cols="9 s:20" responsive="screen" style="align-items: center">
      <template v-for="(info, key) in filteredFoundations" :key="key">
        <n-gi :span="3">
          <n-form-item label-placement="left" :path="'donaco_' + key" :show-feedback="false">
            <n-input-number
              :id="'donaco_' + key"
              v-model:value="form['donaco_' + key]"
              placeholder="0.00"
              :min="0"
              :precision="2"
              :step="0.01"
              :show-button="false"
              :disabled="editMode && !form['donaco_' + key].editable"
            >
              <template #suffix>€</template>
            </n-input-number>
          </n-form-item>
        </n-gi>
        <n-gi :span="6">
          <strong>
            <a v-if="info.url" :href="info.url" target="_blank">{{ info.name }}</a>
            <template v-else>{{ info.name }}</template>
          </strong>
        </n-gi>
        <n-gi span="9 s:11">
          {{ info.description }}
        </n-gi>
      </template>
    </n-grid>
  </n-card>

  <slide-transition>
    <radio-input
      v-if="requiredFields.konsento_donaclisto"
      v-model="form.konsento_donaclisto"
      field-name="konsento_donaclisto"
      :options="formOptions.donationList"
    />
  </slide-transition>

  <table class="price" v-if="!editMode && detailedSum !== null">
    <tr v-for="(row, index) in priceWithLabels" :key="index">
      <td>{{ row.title }}</td>
      <td>{{ row.sum }}&nbsp;€</td>
    </tr>
  </table>
  <div v-if="'sumo' in errors.value" class="sum_error">{{ errors.value.sumo }}</div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import SelectInput from '@/components/form/fields/SelectInput.vue';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import PriceTypeChoice from '@/components/form/parts/PriceTypeChoice.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  errors: Object,
  countryCategory: String,
  requiredFields: Object,
  showPersonalData: Boolean,
  pricesList: Object,
  memberAgeGroup: String,
  detailedSum: Object,
  specialCategory: {
    type: String,
    default: null,
  },
  membershipLocked: Boolean,
});

const form = defineModel('modelValue', Object);

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const fields = computed(() => store.getters.fields);
const editMode = computed(() => store.getters.editMode);

const membrigxo_options = computed(() => {
  const options = {
    [formOptions.value.boolValues.yes]: 'Jes',
    [formOptions.value.boolValues.no]: 'Ne',
  };
  if (props.membershipLocked) {
    options.traktata = 'Mi remembriĝis antaŭnelonge, mia membreco estas traktata';
  }
  return options;
});

const showAsMember = computed(() => {
  if (form.value.membreco === undefined || form.value.membreco === null) {
    return null;
  }
  return (
    form.value.membreco === formOptions.value.boolValues.yes ||
    form.value.volas_membrigxi === formOptions.value.boolValues.yes
  );
});

const filteredFoundations = computed(() => {
  if (!editMode.value) {
    return formOptions.value.foundations;
  }
  // Hide donation fields with 0 if in edit mode because the list would be too long and unnecessary
  const foundations = {};
  for (const [key, value] of Object.entries(formOptions.value.foundations)) {
    if (form.value['donaco_' + key] > 0) {
      foundations[key] = value;
    }
  }
  return foundations;
});

const priceWithLabels = computed(() => {
  if (props.detailedSum === null) {
    return null;
  }
  const price = [{ title: 'Aliĝkotizo', sum: props.detailedSum.aligxkotizo }];
  if ('discount' in props.detailedSum) {
    price.push({ title: 'Rabato pro via partopreno en UK 2025', sum: props.detailedSum.discount });
  }
  if ('membrigxo' in props.detailedSum) {
    price.push({ title: 'Membrokotizo', sum: props.detailedSum.membrigxo });
  }
  Object.entries(props.detailedSum).forEach((entry) => {
    const [key, value] = entry;
    if (key.startsWith('donaco_')) {
      price.push({
        title: fields.value[key].label,
        sum: value,
      });
    }
  });
  price.push({ title: 'Pagenda sumo', sum: props.detailedSum.sum });
  return price;
});

const membercoHelp = computed(() => {
  if (props.membershipLocked) {
    return form.value.membreco === formOptions.value.boolValues.yes
      ? 'Vi jam estas individua membro de UEA.'
      : 'Vi ankoraŭ ne estas individua membro de UEA.';
  }
  return null;
});
</script>

<style scoped lang="scss">
.sum_error {
  color: #d03050;
  padding-top: 0.8rem;
  font-size: 1.1rem;
}

table.price {
  border-collapse: collapse;
  font-size: 1.2em;
  margin-top: 2rem;

  tr {
    vertical-align: top;
  }

  td {
    padding: 3px;
  }

  tr:not(:last-child) td {
    border-bottom: 1px solid #d0d0d0;
  }

  td:not(:first-child) {
    padding-left: 1.6em;
  }

  td:last-child {
    text-align: right;
  }

  tr:last-child {
    font-size: 1.3em;
    font-weight: bold;
  }
}

.custom-card {
  margin-bottom: 2em;
}
</style>
