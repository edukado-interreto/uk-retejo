<template>
  <checkbox-input v-model="form.kompreno_pago" field-name="kompreno_pago" />
  <checkbox-input v-model="form.konsento_aligxlisto" field-name="konsento_aligxlisto" />
  <checkbox-input v-model="form.konsento_kongreslibro" field-name="konsento_kongreslibro" />
  <slide-transition>
    <multi-checkbox-input
      v-if="form.konsento_kongreslibro"
      v-model="form.kongreslibro_adreso"
      field-name="kongreslibro_adreso"
      :options="formOptions.kongreslibro"
    />
  </slide-transition>
  <radio-input v-if="false" v-model="form.konfirmilo" field-name="konfirmilo" :options="formOptions.confirmation" />
  <radio-input v-model="form.fotado" field-name="fotado" :options="formOptions.photo" />

  <n-card class="custom-card margin-bottom" title="Bonvolu atente tralegi la kondiĉojn de aliĝo:" v-if="!editMode">
    <p>
      <strong>La kotizo ne estas repagebla</strong>, senkonsidere ĉu la aliĝinto ne povas partopreni la Kongreson pro
      propra volo aŭ pro iu ajn ekstera kaŭzo, eĉ se la Kongreso ne okazas, aŭ okazas en alia urbo.
    </p>
    <p>
      <strong>La kotizo ne inkluzivas</strong> loĝadon, ekskursojn, bankedon kaj eventuale aliajn aparte pagendajn
      aferojn pri kiuj informoj kaj mendiloj aperas en la Dua Bulteno. La kotizo inkluzivas nenian asekuron.
    </p>
    <p>
      <strong>Kongresaneco ne estas transdonebla al alia persono.</strong> Fraŭdo kun la nomŝildo estas punebla per
      konfisko de la nomŝildo kaj malpermeso al la fraŭdanto(j) plu partopreni tiun kongreson.
    </p>
    <p>
      <strong>
        Por la limdatoj kaj aliaj kondiĉoj validas la dato de ricevo de la pago en la
        <abbr title="Centra Oficejo">CO</abbr> aŭ ĉe peranto. Aliĝilon sen kompleta pago aŭ pago sen (subskribita)
        aliĝilo oni ne traktos.
      </strong>
    </p>
    <p>
      <strong>Fotado kaj filmado.</strong> Dum la Kongreso UEA faros oficialajn fotojn kaj videoregistraĵojn, kiuj povas
      inkluzivi partoprenantojn. UEA povas uzi ilin por dokumenti kaj reklami ĉi tiun kaj estontajn Kongresojn,
      inkluzive en retejoj, sociaj retoj kaj aliaj publikaĵoj. Ankaŭ prelegoj kaj aliaj programeroj povas esti oficiale
      registrataj kaj poste publikigataj rete. Se vi ne volas esti fotata aŭ filmata, vi povas indiki tion ĉi-supre, vi
      tiam ricevos specialan signon sur la nomŝildo. Tiu elekto devas esti respektata dum la Kongreso, ankaŭ de aliaj
      partoprenantoj. En grandaj salonoj kaj grupaj fotoj vi tamen povas aperi en la fono. Vian elekton vi povas ŝanĝi
      uzante vian personan ligilon el la konfirma retmesaĝo, post la presado de la nomŝildoj turnu vin ankaŭ al la
      akceptejo.
    </p>
    <p>
      <strong>Propraj fotoj kaj filmoj.</strong> Partoprenantoj rajtas fari fotojn kaj mallongajn filmetojn; dum
      programeroj oni filmu nur mallongajn fragmentojn (ĝis ĉ. 1 minuto), krom se la organizantoj permesas pli longan
      registradon. Privatajn interparolojn kaj fermitajn kunsidojn oni ne registru sen permeso de ĉiuj ĉeestantoj.
      Fotante aŭ filmante aliajn homojn, oni devas respekti ilian privatecon kaj iliajn petojn ne esti fotataj aŭ
      filmataj, ankaŭ kiam oni publikigas fotojn.
    </p>
    <p>
      <strong>
        <a href="https://uea.org/teko/regularoj/kongresa_regularo#a2" target="_blank">Kongresa Regularo</a>
        (ekstrakto):
      </strong>
      <q>
        2.4. Kongresanoj devas fari nenion, kio kontraŭas la Kongresan Regularon, aŭ malutilas al la UK, kaj devas
        submetiĝi al la leĝoj de la lando, kie okazas la UK.
      </q>
    </p>
    <p>
      La klarigon pri datumprotektado de UEA vi povas legi
      <strong><a href="https://uea.org/teko/regularoj/datumprotektado" target="_blank">en la retejo de UEA</a></strong
      >.
    </p>
  </n-card>

  <checkbox-input v-model="form.akcepto_reguloj" field-name="akcepto_reguloj" />
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import MultiCheckboxInput from '@/components/form/fields/MultiCheckboxInput.vue';
import CheckboxInput from '@/components/form/fields/CheckboxInput.vue';

const form = defineModel({ type: Object, required: true });

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const editMode = computed(() => store.getters.editMode);
</script>
