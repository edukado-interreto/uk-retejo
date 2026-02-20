<template>
  <p>
    Sur la nomŝildo aperos via plena nomo, UEA-kodo kaj la kongresa numero. Ĉi tie vi povas enmeti nomon, kiu estos
    presita pli grande – kutime la persona nomo.
  </p>
  <p>Tiuj ĉi informoj estos presitaj sur vian nomŝildon. Bone pripensu!</p>

  <n-grid x-gap="12" cols="1 s:2" responsive="screen">
    <n-gi>
      <text-input
        v-model="form.sxildonomo"
        field-name="sxildonomo"
        help="Povas esti via persona nomo, via plena nomo, kromnomo…"
        autocapitalize="words"
      />
    </n-gi>
    <n-gi>
      <text-input
        v-model="form.sxildolando"
        field-name="sxildolando"
        help="Povas esti via devenlando, via loĝlando, ambaŭ…"
        autocapitalize="words"
      />
    </n-gi>
  </n-grid>
</template>

<script>
import TextInput from '@/components/form/fields/TextInput.vue';

export default {
  components: { TextInput },
  props: {
    modelValue: Object,
  },
  emits: ['update:modelValue'],
  name: 'FormNametag',
  computed: {
    form: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
};
</script>

<style scoped></style>
