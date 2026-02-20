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
              :checked="modelValue === key"
              :value="key"
              :name="fieldName"
              :disabled="!isEditable"
              @change="modelValue = key"
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
              (key === 'kunulo' && modelValue === 'kunulo') || (key === 'akompananto' && modelValue === 'akompananto')
            "
            offset="0 s:2"
            span="3 s:8"
          >
            <text-input
              v-model="cxefaligxinto"
              field-name="cxefaligxinto"
              :manual-error="cxefaligxintoError"
              required
            />
          </n-gi>
          <n-gi v-else-if="key === 'handikapulo' && modelValue === 'handikapulo'" offset="0 s:2" span="3 s:8">
            <radio-input v-model="handikapatestilo" field-name="handikapatestilo" :options="formOptions.handicap" />
          </n-gi>
          <n-gi
            v-else-if="
              ((key === 'junulo' && modelValue === 'junulo') || (key === 'infano' && modelValue === 'infano')) &&
              (birthday === null || birthday === '') &&
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

const props = defineProps({
  fieldName: String,
  memberAgeGroup: String,
  birthday: String,
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
  uea_kodo: {
    type: String,
    default: null,
  },
  fullName: {
    type: String,
    default: null,
  },
  pricesList: Object,
  specialCategory: {
    type: String,
    default: null,
  },
});

const modelValue = defineModel({ type: String });

const cxefaligxinto = defineModel('cxefaligxinto', String);
const handikapatestilo = defineModel('handikapatestilo', String);

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const fields = computed(() => store.getters.fields);
const editMode = computed(() => store.getters.editMode);

const field = computed(() => fields.value[props.fieldName]);
const isEditable = computed(() => !editMode.value || field.value.editable !== false);

const showYouth = computed(() =>
  isYouth(props.birthday, props.showPersonalData, props.memberAgeGroup, formOptions.value),
);
const showChild = computed(() =>
  isChild(props.birthday, props.showPersonalData, props.memberAgeGroup, formOptions.value),
);

const cxefaligxintoError = computed(() => {
  if (!props.cxefaligxinto) {
    return null;
  }
  if (
    (props.uea_kodo && props.uea_kodo === props.cxefaligxinto) ||
    (props.fullName && props.fullName === props.cxefaligxinto)
  ) {
    return 'Vi ne povas esti via propra ' + modelValue.value + '.';
  }
  return null;
});

const filteredPricesList = computed(() => {
  const list = {};
  for (const [key, value] of Object.entries(props.pricesList)) {
    if (value.public || key === props.specialCategory || (editMode.value && modelValue.value === key)) {
      if (!(key === 'junulo' && !showYouth.value) && !(key === 'infano' && !showChild.value)) {
        list[key] = value;
      }
    }
  }
  return list;
});

watch(
  () => filteredPricesList.value,
  (newList) => {
    if (!(modelValue.value in newList)) {
      modelValue.value = 'baza';
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
