<template>
  <n-form-item
      :required="isRequired"
      :path="fieldName"
      :feedback="help"
      label-placement="left"
  >
    <n-checkbox
        v-model:checked="value"
        :id="fieldName"
        :disabled="!isEditable"
        @update:checked="v => $emit('update:modelValue', v)"
    >
      {{ label }}<span v-if="isRequired" class="n-form-item-label__asterisk">&nbsp;*</span>
    </n-checkbox>
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
    help: {
      type: String,
      default: null
    }
  },
  inject: ['formErrors'],
  data() {
    return {
      value: this.modelValue
    }
  },
  computed: {
    ...mapGetters([
      'fields',
      'editMode'
    ]),
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
  }
}
</script>

<style scoped>
.n-form-item-label__asterisk {
  user-select: none;
  -webkit-user-select: none;
  color: var(--n-asterisk-color);
  transition: color .3s var(--n-bezier);
}
</style>