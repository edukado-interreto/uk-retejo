<template>
  <n-form-item :required="isRequired" :path="fieldName" :feedback="feedback" label-placement="left">
    <n-checkbox v-model:checked="modelValue" :id="fieldName" :disabled="!isEditable">
      <span v-html="label"></span>
      <span v-if="isRequired" class="n-form-item-label__asterisk">&nbsp;*</span>
    </n-checkbox>
  </n-form-item>
</template>

<script setup>
import { computed, inject } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  modelValue: String,
  fieldName: String,
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  help: {
    type: String,
    default: null,
  },
});

const store = useStore();
const fields = computed(() => store.getters.fields);
const editMode = computed(() => store.getters.editMode);

const modelValue = defineModel('modelValue');

const field = computed(() => fields.value[props.fieldName]);
const isRequired = computed(
  () =>
    props.required ||
    ('validation_rules' in field.value && Object.values(field.value.validation_rules).includes('required')),
);

const isEditable = computed(() => !editMode.value || field.value.editable !== false);
const label = computed(() => {
  let l = props.label ? props.label : field.value.label;
  l = l.replace('(nedevige)', '<span style="color: var(--n-feedback-text-color); font-size: .9em;">(nedevige)</span>');
  return l;
});

const formErrors = inject('formErrors');
const hasError = computed(() => props.fieldName in formErrors.value);
const error = computed(() => (hasError.value ? formErrors.value[props.fieldName] : ''));
const feedback = computed(() => (hasError.value ? error.value : props.help));
</script>

<style scoped>
.n-form-item-label__asterisk {
  user-select: none;
  -webkit-user-select: none;
  color: var(--n-asterisk-color);
  transition: color 0.3s var(--n-bezier);
}
</style>
