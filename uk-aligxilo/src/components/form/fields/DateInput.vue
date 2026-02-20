<template>
  <n-form-item
      :label="label"
      :required="isRequired"
      :path="fieldName"
      :feedback="help"
  >
    <n-date-picker
        v-model:formatted-value="fieldValue"
        :id="fieldName"
        :placeholder="placeholder"
        :clearable="clearable"
        :is-date-disabled="dateDisabled"
        :disabled="!isEditable"
        type="date"
        value-format="yyyy-MM-dd"
        :actions="['clear']"
    />
  </n-form-item>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "DateInput",
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
  methods: {
    dateDisabled(ts) {
      let maxDate;
      if (this.max === 'now') {
        maxDate = new Date();
      }
      else if (this.max === null) {
        maxDate = new Date('2999-12-31T00:00:00.000');
      }
      else {
        maxDate = new Date(this.max + 'T00:00:00.000');
      }

      let minDate;
      if (this.min === 'now') {
        minDate = new Date();
      }
      else if (this.min === null) {
        minDate = new Date('0001-01-01T00:00:00.000');
      }
      else {
        minDate = new Date(this.min + 'T00:00:00.000');
      }
      const date = new Date(ts);
      return date.getTime() < minDate.getTime() || date.getTime() > maxDate.getTime();
    }
  }
}
</script>
