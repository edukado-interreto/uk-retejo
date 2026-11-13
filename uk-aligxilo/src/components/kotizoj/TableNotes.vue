<script setup>
import { NCollapse, NCollapseItem } from 'naive-ui';

defineProps({
  isMobile: { type: Boolean, default: false },
});
</script>

<template>
  <div class="kt-notes">
    <!-- La regulo pri la dato de pago estas ĉiam videbla, ĉar ĝi influas la prezon. -->
    <p>Por la aliĝperiodo decidas la dato, kiam via pago alvenas al CO aŭ al peranto, ne la dato de la aliĝilo.</p>

    <template v-if="!isMobile">
      <p>A kaj B estas landokategorioj. Emfazita estas la kolumno de via lando. <a href="#kt-landoj">Ĉiuj landoj</a></p>
      <p>
        Membro de UEA signifas individuan membron de UEA (dumvivan, bazan aŭ abonantan) en la momento de aliĝo. Membroj
        nur de landa asocio (aligitaj membroj) pagas kiel nemembroj. Se vi volas membriĝi, vi povas fari tion rekte en
        la aliĝilo.
      </p>
    </template>

    <n-collapse v-else>
      <n-collapse-item title="Klarigoj al la tabelo" name="klarigoj">
        <p>
          A kaj B estas landokategorioj. Emfazita estas la kolumno de via lando. <a href="#kt-landoj">Ĉiuj landoj</a>
        </p>
        <p>
          Membro de UEA signifas individuan membron de UEA (dumvivan, bazan aŭ abonantan) en la momento de aliĝo.
          Membroj nur de landa asocio (aligitaj membroj) pagas kiel nemembroj. Se vi volas membriĝi, vi povas fari tion
          rekte en la aliĝilo.
        </p>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>
