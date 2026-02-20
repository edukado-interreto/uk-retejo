<template>
  <checkbox-input
      v-model="form.kompreno_pago"
      field-name="kompreno_pago"
  />
  <checkbox-input
      v-model="form.konsento_aligxlisto"
      field-name="konsento_aligxlisto"
  />
  <checkbox-input
      v-model="form.konsento_kongreslibro"
      field-name="konsento_kongreslibro"
  />
  <slide-transition>
    <multi-checkbox-input
        v-if="form.konsento_kongreslibro"
        v-model="form.kongreslibro_adreso"
        field-name="kongreslibro_adreso"
        :options="formOptions.kongreslibro"
    />
  </slide-transition>
  <radio-input v-if="false"
      v-model="form.konfirmilo"
      field-name="konfirmilo"
      :options="formOptions.confirmation"
  />

  <n-card class="custom-card margin-bottom" title="Bonvolu atente tralegi la kondiĉojn de aliĝo:" v-if="!editMode">
    <p><strong>La kotizo ne estas repagebla</strong>, senkonsidere ĉu la aliĝinto ne povas partopreni la Kongreson pro propra volo aŭ pro iu ajn ekstera kaŭzo, eĉ se la Kongreso ne okazas, aŭ okazas en alia urbo.</p>
    <p><strong>La kotizo ne inkluzivas</strong> loĝadon, ekskursojn, bankedon kaj eventuale aliajn aparte pagendajn aferojn pri kiuj informoj kaj mendiloj aperas en la Dua Bulteno. La kotizo inkluzivas nenian asekuron.</p>
    <p><strong>Kongresaneco ne estas transdonebla al alia persono.</strong> Fraŭdo kun la nomŝildo estas punebla per konfisko de la nomŝildo kaj malpermeso al la fraŭdanto(j) plu partopreni tiun kongreson.</p>
    <p><strong>Por la limdatoj kaj aliaj kondiĉoj validas la dato de ricevo de la pago en la <abbr title="Centra Oficejo">CO</abbr> aŭ ĉe peranto. Aliĝilon sen kompleta pago aŭ pago sen (subskribita) aliĝilo oni ne traktos.</strong> </p>
    <p><strong><a href="https://uea.org/teko/regularoj/kongresa_regularo#a2" target="_blank">Kongresa Regularo</a> (ekstrakto):</strong> <q>2.4. Kongresanoj devas fari nenion, kio kontraŭas la Kongresan Regularon, aŭ malutilas al la UK, kaj devas submetiĝi al la leĝoj de la lando, kie okazas la UK.</q></p>
    <p>La klarigon pri datumprotektado de UEA vi povas legi <strong><a
        href="https://uea.org/teko/regularoj/datumprotektado" target="_blank">en la retejo de UEA</a></strong>.</p>
  </n-card>

  <checkbox-input
      v-model="form.akcepto_reguloj"
      field-name="akcepto_reguloj"
  />
</template>

<script>
import RadioInput from "@/components/form/fields/RadioInput.vue";
import SlideTransition from "@/components/ui/SlideTransition.vue";
import MultiCheckboxInput from "@/components/form/fields/MultiCheckboxInput.vue";
import CheckboxInput from "@/components/form/fields/CheckboxInput.vue";
import {mapGetters} from "vuex";

export default {
  components: {CheckboxInput, MultiCheckboxInput, SlideTransition, RadioInput},
  props: {
    modelValue: Object,
  },
  emits: ['update:modelValue'],
  name: "FormConditions",
  computed: {
    ...mapGetters([
      'formOptions',
      'editMode'
    ]),
    form: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  }
}
</script>

<style scoped>

</style>