<script setup>
import { computed } from 'vue';
import {
  IconRun,
  IconHomeHeart,
  IconDisabled,
  IconUsersGroup,
  IconMoodKid,
  IconHeartHandshake,
} from '@tabler/icons-vue';

const props = defineProps({
  junulo: { type: Object, required: true }, // { de: 'YYYY-MM-DD', gxis: 'YYYY-MM-DD' }
  senpagePost: { type: String, required: true },
});

const rabataj = computed(() => [
  {
    icon: IconRun,
    title: 'Junulo',
    text: `Persono, kiu naskiĝis inter ${props.junulo.de} kaj ${props.junulo.gxis}. Indiku la naskiĝdaton en la aliĝilo kaj sendu kopion de identigilo.`,
  },
  {
    icon: IconHomeHeart,
    title: 'Kunulo',
    text: 'Persono, kiu loĝas ĉe la sama adreso kiel ĉefaliĝinto (persono, kiu pagas plenan kotizon kiel membro aŭ nemembro).',
  },
  {
    icon: IconDisabled,
    title: 'Handikapulo',
    text: 'Persono, kiu nepre bezonas akompananton (ekzemple blindulo) kaj pruvas tion per kuracista aŭ simila atestilo.',
  },
  {
    icon: IconUsersGroup,
    title: 'Komitatano',
    text: 'Persono, kiu estas membro aŭ observanto en la Komitato de UEA en la momento de la aliĝo kaj samtempe individua membro de UEA.',
  },
]);

const senpagaj = computed(() => [
  { icon: IconMoodKid, title: 'Infano aŭ adoleskulo', text: `Persono, kiu naskiĝis post ${props.senpagePost}.` },
  {
    icon: IconHeartHandshake,
    title: 'Akompananto de handikapulo',
    text: 'Persono, kiu akompanas handikapulon, kies handikapo nepre postulas akompananton.',
  },
]);
</script>

<template>
  <section id="kt-rabatoj" class="kt-section" aria-labelledby="kt-h-rabatoj">
    <h2 id="kt-h-rabatoj" class="kt-h2">Kiu rajtas je rabatita kotizo?</h2>
    <div class="kt-grid kt-grid--4">
      <article v-for="c in rabataj" :key="c.title" class="kt-cardbox">
        <div class="kt-cardbox__head">
          <component :is="c.icon" :size="26" :stroke-width="1.8" aria-hidden="true" />
          <h3>{{ c.title }}</h3>
        </div>
        <p>{{ c.text }}</p>
      </article>
    </div>
  </section>

  <section class="kt-section" aria-labelledby="kt-h-senpage">
    <h2 id="kt-h-senpage" class="kt-h2">Kiu aliĝas senpage?</h2>
    <div class="kt-grid kt-grid--2">
      <article v-for="c in senpagaj" :key="c.title" class="kt-cardbox">
        <div class="kt-cardbox__head">
          <component :is="c.icon" :size="26" :stroke-width="1.8" aria-hidden="true" />
          <h3>{{ c.title }}</h3>
        </div>
        <p>{{ c.text }}</p>
      </article>
    </div>
    <p class="kt-text">Ankaŭ por senpaga partopreno necesas aliĝi per la aliĝilo.</p>
  </section>
</template>
