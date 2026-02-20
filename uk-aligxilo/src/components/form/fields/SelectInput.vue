<template>
  <n-form-item
    :label="label"
    :required="isRequired"
    :path="fieldName"
    :feedback="feedback"
    :validation-status="validationStatus"
  >
    <n-select
      v-model:value="modelValue"
      :id="fieldName"
      :placeholder="placeholder"
      :options="optionsListWithDisabled"
      :clearable="clearable"
      :filterable="filterable"
      :disabled="disabled || !isEditable"
      :style="style"
    />
  </n-form-item>
</template>

<script setup>
import { computed, inject } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  modelValue: String,
  fieldName: String,
  options: [Object, Array],
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: false,
  },
  filterable: {
    type: Boolean,
    default: false,
  },
  help: {
    type: String,
    default: null,
  },
  placeholder: {
    type: String,
    default: null,
  },
  width: {
    type: String,
    default: null,
  },
  disabledOptions: {
    type: Array,
    default: () => [],
  },
  label: {
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

const label = computed(() => (props.label ? props.label : field.value.label));

const hasError = computed(() => props.fieldName in formErrors.value);
const error = computed(() => (hasError.value ? props.manualError || formErrors.value[field.valueName] : ''));
const validationStatus = computed(() => (hasError.value ? 'error' : null));
const feedback = computed(() => (hasError.value ? error.value : props.help));

// Component-specific properties

const optionsList = computed(() => {
  if (Array.isArray(props.options)) {
    return props.options.map((option) => {
      if (typeof option === 'object') {
        return option;
      }
      return {
        value: option,
        label: option,
      };
    });
  }
  return Object.keys(props.options).map((key) => {
    return {
      value: key,
      label: props.options[key],
    };
  });
});

const optionsListWithDisabled = computed(() =>
  optionsList.value.map((o) => {
    if (props.disabledOptions.includes(o.value)) {
      o.disabled = true;
    }
    return o;
  }),
);
const style = computed(() => {
  return {
    maxWidth: props.width,
  };
});
</script>
