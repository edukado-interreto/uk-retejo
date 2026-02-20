<template>
  <n-form-item
    :label="label"
    :required="isRequired"
    :path="fieldName"
    :feedback="feedback"
    :validation-status="validationStatus"
  >
    <n-input-number
      :id="fieldName"
      :min="min"
      :placeholder="placeholder"
      :value="modelValue"
      @update:value="(v) => $emit('update:modelValue', v)"
      :disabled="!isEditable"
    >
      <template #suffix> € </template>
    </n-input-number>
  </n-form-item>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'NumberInput',
  props: {
    modelValue: String,
    fieldName: String,
    required: {
      type: Boolean,
      default: false,
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
  },
  inject: ['formErrors'],
  computed: {
    ...mapGetters(['fields', 'editMode']),
    field() {
      return this.fields[this.fieldName];
    },
    isRequired() {
      return (
        this.required ||
        ('validation_rules' in this.field && Object.values(this.field.validation_rules).includes('required'))
      );
    },
    isEditable() {
      return !this.editMode || this.field.editable !== false;
    },
    min() {
      if ('validation_rules' in this.field && 'min_numeric' in this.field.validation_rules) {
        return this.field.validation_rules.min_numeric;
      }
      return null;
    },
    label() {
      if (this.defaultLabel !== null) {
        return this.defaultLabel;
      }
      return this.field.label;
    },
    hasError() {
      return this.manualError !== null || this.fieldName in this.formErrors.value;
    },
    error() {
      return this.hasError ? this.manualError || this.formErrors.value[this.fieldName] : '';
    },
    validationStatus() {
      if (this.hasError) {
        return 'error';
      }
      return null;
    },
    feedback() {
      if (this.hasError) {
        return this.error;
      }
      return this.help;
    },
  },
  mounted() {
    if ((this.type === 'text' || this.type === 'tel') && this.modelValue !== undefined) {
      this.$emit('update:modelValue', this.modelValue.toString()); // Avoid bugs if it's a number
    }
  },
};
</script>

<style scoped></style>
