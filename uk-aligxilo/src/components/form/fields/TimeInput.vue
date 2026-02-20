<template>
  <n-form-item
      :label="label"
      :required="isRequired"
      :path="fieldName"
      :feedback="help"
  >
    <n-time-picker
        v-model:formatted-value="fieldValue"
        :id="fieldName"
        :placeholder="placeholder"
        :disabled="!isEditable"
        :actions="['clear']"
        :clearable="true"
        :minutes="5"
        :seconds="[0]"
        format="HH:mm"
    />
  </n-form-item>
</template>

<script>
import {mapGetters} from "vuex";
import {NTimePicker} from "naive-ui";

export default {
  name: "TimeInput",
  components: { NTimePicker },
  props: {
    modelValue: String,
    fieldName: String,
    type: {
      type: String,
      default: "text"
    },
    required: {
      type: Boolean,
      default: false
    },
    clearable: {
      type: Boolean,
      default: false
    },
    help: {
      type: String,
      default: null
    },
    placeholder: {
      type: String,
      default: null
    },
    min: {
      type: String,
      default: null
    },
    max: {
      type: String,
      default: null
    },
  },
  inject: ['formErrors'],
  computed: {
    ...mapGetters([
      'fields',
      'editMode'
    ]),
    fieldValue: {
      get() {
        if (this.modelValue === '') {
          return null;
        }
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    },
    field() {
      return this.fields[this.fieldName];
    },
    isRequired() {
      return this.required || ('validation_rules' in this.field && Object.values(this.field.validation_rules).includes('required'));
    },
    isEditable() {
      return !this.editMode || this.field.editable !== false;
    },
    label() {
      return this.field.label;
    },
    hasError() {
      return this.fieldName in this.formErrors.value;
    },
    error() {
      return this.hasError ? this.formErrors.value[this.fieldName] : '';
    }
  },
}
</script>
