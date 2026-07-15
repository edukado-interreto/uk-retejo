<template>
  <n-card class="custom-card" :title="field.label">
    <n-form-item :required="required" :path="fieldName">
      <n-grid x-gap="12" y-gap="16" cols="3 s:10" responsive="screen" style="align-items: center">
        <n-gi span="0 s:6" offset="4" style="text-align: right; margin-top: -3rem; margin-bottom: -1.5rem">
          <strong>Ĉu vi estas individua membro de UEA?</strong>
        </n-gi>
        <n-gi span="0 s:1" offset="8" :class="{ price: true, disabled: membership === false }">
          <strong>Jes</strong>
          <n-tooltip trigger="hover">
            <template #trigger>
              <span class="trigger">?</span>
            </template>
            {{ formOptions.membership[formOptions.boolValues.yes] }}
          </n-tooltip>
        </n-gi>
        <n-gi span="0 s:1" :class="{ price: true, disabled: membership === true }">
          <strong>Ne</strong>
          <n-tooltip trigger="hover">
            <template #trigger>
              <span class="trigger">?</span>
            </template>
            {{ formOptions.membership[formOptions.boolValues.no] }}
          </n-tooltip>
        </n-gi>
        <template v-for="(info, key) in filteredPricesList" :key="key">
          <n-gi :span="2">
            <n-radio
              :checked="form.kotizo === key"
              :value="key"
              :name="fieldName"
              :disabled="!isEditable"
              @change="form.kotizo = key"
            >
              <strong>{{ info.name }}</strong>
            </n-radio>
          </n-gi>
          <n-gi span="0 s:6">{{ info.description }}</n-gi>
          <n-gi span="0 s:1" :class="{ price: true, disabled: membership === false }">
            <strong>{{ info.priceM }}</strong
            >&nbsp;€
          </n-gi>
          <n-gi span="0 s:1" :class="{ price: true, disabled: membership === true }">
            <strong>{{ info.priceNM }}</strong
            >&nbsp;€
          </n-gi>
          <n-gi span="1 s:0"
            ><strong>{{ info.price }}</strong
            >&nbsp;€</n-gi
          >
          <n-gi span="3 s:0">{{ info.description }}</n-gi>

          <n-gi
            v-if="
              (key === 'kunulo' && form.kotizo === 'kunulo') || (key === 'akompananto' && form.kotizo === 'akompananto')
            "
            offset="0 s:2"
            span="3 s:8"
          >
            <text-input
              v-model="form.cxefaligxinto"
              field-name="cxefaligxinto"
              :manual-error="cxefaligxintoError"
              required
            />
          </n-gi>
          <n-gi v-else-if="key === 'handikapulo' && form.kotizo === 'handikapulo'" offset="0 s:2" span="3 s:8">
            <radio-input
              v-model="form.handikapatestilo"
              field-name="handikapatestilo"
              :options="formOptions.handicap"
            />
          </n-gi>
          <n-gi
            v-else-if="
              ((key === 'junulo' && form.kotizo === 'junulo') || (key === 'infano' && form.kotizo === 'infano')) &&
              (form.birthday === null || form.birthday === '') &&
              showBirthDateWarning
            "
            span="3 s:10"
          >
            <n-alert type="warning">
              Nepre indiku vian naskiĝdaton en la kadro “Personaj informoj pri la aliĝanto”.
            </n-alert>
          </n-gi>
        </template>
      </n-grid>
    </n-form-item>
  </n-card>
</template>

<script setup>
import { computed, watch } from 'vue';
import { useStore } from 'vuex';
import { isYouth, isChild } from '@/helpers/price.js';
import TextInput from '../fields/TextInput.vue';
import RadioInput from '../fields/RadioInput.vue';
import { numberOfDays } from '@/helpers/time.js';

const props = defineProps({
  fieldName: String,
  memberAgeGroup: String,
  required: {
    type: Boolean,
    default: false,
  },
  showBirthDateWarning: {
    type: Boolean,
    default: false,
  },
  membership: {
    type: Boolean,
    default: false,
  },
  pricesList: Object,
  specialCategory: {
    type: String,
    default: null,
  },
});

const form = defineModel({ type: String });

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const fields = computed(() => store.getters.fields);
const editMode = computed(() => store.getters.editMode);

const field = computed(() => fields.value[props.fieldName]);
const isEditable = computed(() => !editMode.value || field.value.editable !== false);

const showYouth = computed(() =>
  isYouth(form.value.birthday, props.showPersonalData, props.memberAgeGroup, formOptions.value),
);
const showChild = computed(() =>
  isChild(form.value.birthday, props.showPersonalData, props.memberAgeGroup, formOptions.value),
);

const cxefaligxintoError = computed(() => {
  if (!form.value.cxefaligxinto) {
    return null;
  }
  if (
    (form.value.uea_kodo && form.value.uea_kodo === form.value.cxefaligxinto) ||
    (fullName.value && fullName.value === form.value.cxefaligxinto)
  ) {
    return 'Vi ne povas esti via propra ' + form.value.kotizo + '.';
  }
  return null;
});

const filteredPricesList = computed(() => {
  let partialPriceMember = 9999999;
  let partialPriceNonMember = 9999999;
  const days = numberOfDays(form.value.partopreno_de, form.value.partopreno_gxis);
  if (days > 0 && days < 3) {
    partialPriceMember = days * formOptions.value.dayPriceMember;
    partialPriceNonMember = days * formOptions.value.dayPriceNonmember;
  }

  const list = {};
  for (const [key, value] of Object.entries(props.pricesList)) {
    if (value.public || key === props.specialCategory || (editMode.value && form.value.kotizo === key)) {
      if (!(key === 'junulo' && !showYouth.value) && !(key === 'infano' && !showChild.value)) {
        list[key] = { ...value };
        list[key].priceM = Math.min(value.priceM, partialPriceMember);
        list[key].priceNM = Math.min(value.priceNM, partialPriceNonMember);
      }
    }
  }
  return list;
});

const fullName = computed(() => (form.value.persona_nomo ? form.value.familia_nomo.trim() : ''));

watch(
  () => filteredPricesList.value,
  (newList) => {
    if (!(form.value.kotizo in newList)) {
      form.value.kotizo = 'baza';
    }
  },
);
</script>

<style scoped>
.price {
  text-align: right;
}

.disabled {
  color: var(--n-feedback-text-color);
}

.trigger {
  background: rgba(38, 38, 38, 0.95);
  color: white;
  font-weight: bold;
  border-radius: 50%;
  padding: 1px 0.47rem;
  margin-left: 0.4rem;
  cursor: help;
}

.disabled .trigger {
  background: var(--n-feedback-text-color);
}
</style>
