<template>
  <n-form-item
    :label="label"
    :required="isRequired"
    :path="fieldName"
    :feedback="feedback"
    :validation-status="validationStatus"
  >
    <n-input
      :id="fieldName"
      :type="type"
      :maxlength="maxlength"
      :input-props="inputProps"
      :placeholder="placeholder"
      v-model:value="modelValue"
      :disabled="!isEditable"
    />
  </n-form-item>
</template>

<script setup>
import { computed, inject, onMounted } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  fieldName: String,
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  autocapitalize: {
    type: String,
    default: null,
  },
  placeholder: {
    type: String,
    default: null,
  },
  defaultLabel: {
    type: String,
    default: null,
  },
  help: {
    type: String,
    default: null,
  },
  manualError: {
    type: String,
    default: null,
  },
});

const modelValue = defineModel('modelValue', String);

const store = useStore();
const fields = computed(() => store.getters.fields);
const field = computed(() => fields.value[props.fieldName]);
const editMode = computed(() => store.getters.editMode);

const formErrors = inject('formErrors');

const isRequired = computed(
  () =>
    props.required ||
    ('validation_rules' in field.value && Object.values(field.value.validation_rules).includes('required')),
);

const isEditable = computed(() => !editMode.value || field.value.editable !== false);

const maxlength = computed(() => {
  if ('validation_rules' in field.value && 'max_len' in field.value.validation_rules) {
    return field.value.validation_rules.max_len;
  } else if ('validation_rules' in field.value && 'exact_len' in field.value.validation_rules) {
    return field.value.validation_rules.exact_len;
  }
  return null;
});

const label = computed(() => {
  if (props.defaultLabel !== null) {
    return props.defaultLabel;
  }
  return field.value.label;
});

const hasError = computed(() => props.manualError !== null || props.fieldName in formErrors.value);
const error = computed(() => (hasError.value ? props.manualError || formErrors.value[field.valueName] : ''));
const validationStatus = computed(() => (hasError.value ? 'error' : null));
const feedback = computed(() => (hasError.value ? error.value : props.help));

const inputProps = computed(() => {
  const attributes = {};
  if (props.autocapitalize) {
    attributes.autocapitalize = props.autocapitalize;
  }
  return attributes;
});

onMounted(() => {
  if ((props.type === 'text' || props.type === 'tel') && modelValue.value !== undefined) {
    modelValue.value = modelValue.value.toString(); // Avoid bugs if it's a number
  }
});
</script>

<style scoped></style>
