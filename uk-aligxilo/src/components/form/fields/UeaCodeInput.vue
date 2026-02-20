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
      maxlength="6"
      placeholder="xxxx-x"
      :value="modelValue"
      @input="checkUeaCode"
      autosize
      :loading="loading"
      :readonly="loading"
      :disabled="!isEditable"
      :style="{ minWidth: '7.8em', fontSize: '1.4em' }"
      size="large"
      :input-props="{ autocapitalize: 'off' }"
    />
  </n-form-item>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  name: 'UeaCodeInput',
  emits: ['update:modelValue', 'codeChecked'],
  props: {
    modelValue: String,
    fieldName: String,
    mode: {
      type: String,
      default: null,
    },
    currentUser: {
      type: String,
      default: null,
    },
    required: {
      type: Boolean,
      default: false,
    },
    help: {
      type: String,
      default: null,
    },
    categoryToCheck: {
      // E.g. "handikapulo" if user has to be in the list of handicapped users
      type: String,
      default: null,
    },
    manualError: {
      type: String,
      default: null,
    },
  },
  inject: ['formErrors'],
  data() {
    return {
      loading: false,
      correct: false,
      incorrect: false,
      alreadyBooked: false,
    };
  },
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
    label() {
      return this.field.label;
    },
    hasError() {
      return this.manualError !== null || this.fieldName in this.formErrors.value;
    },
    error() {
      return this.hasError ? this.manualError || this.formErrors.value[this.fieldName] : '';
    },
    validationStatus() {
      if (this.hasError || this.incorrect) {
        return 'error';
      }
      if (this.correct) {
        return 'success';
      }
      return null;
    },
    feedback() {
      if (this.hasError) {
        return this.error;
      }
      if (this.alreadyBooked) {
        return 'Ĉi tiu partoprenanto jam havas mendon';
      }
      if (this.incorrect && this.mode === null) {
        return 'Malĝusta UEA-kodo';
      }
      if (this.incorrect) {
        return 'Malĝusta UEA-kodo aŭ ĉi tiu persono ankoraŭ ne kongresaniĝis';
      }
      if (this.correct) {
        return 'Ĝusta UEA-kodo';
      }
      return this.help;
    },
  },
  methods: {
    checkUeaCode(v) {
      this.$emit('update:modelValue', v);
      const regex = new RegExp('^[a-z]{4}-[a-z]$');
      if (!regex.test(v.toLowerCase())) {
        this.$emit('codeChecked', { valid: false });
        this.incorrect = false;
        this.correct = false;
      } else {
        this.loading = true;

        const url = this.mode === null ? '/checkcode' : '/checkcode/booking';
        const postData = { code: v };
        if (this.mode !== null) {
          postData.currentUser = this.currentUser;
          postData.mode = this.mode;
        }

        axios
          .post(url, postData)
          .then((result) => {
            this.$emit('codeChecked', result.data);
            this.correct = result.data.valid;
            if (this.correct && this.categoryToCheck !== null) {
              this.correct = result.data.member.specialCategory === this.categoryToCheck;
            }
            this.incorrect = !this.correct;
            this.alreadyBooked = 'alreadyBooked' in result.data && result.data.alreadyBooked;
            if ('redirect' in result.data.member) {
              window.location = result.data.member.redirect;
            }
          })
          .catch(() => {
            this.$emit('codeChecked', { valid: false });
            this.incorrect = true;
            this.correct = false;
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
  },
};
</script>

<style scoped></style>
