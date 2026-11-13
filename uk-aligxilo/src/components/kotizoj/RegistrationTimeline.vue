<script setup>
// Fazoj kaj paŝoj. "optional" fazo estas desegnita per streka linio.
const phases = [
  {
    title: 'Aliĝo al la kongreso',
    tone: 'main',
    steps: [
      { text: 'Vi plenigas la aliĝilon kaj ricevas aŭtomatan konfirmon retpoŝte.', width: 1.85 },
      { text: 'Vi pagas la kotizon.', width: 1 },
      { text: 'UEA registras vian pagon.', width: 1.05 },
      { text: 'Vi ricevas konfirman retmesaĝon kun via kongresa numero kaj persona ligilo.', width: 2.1 },
    ],
  },
  {
    title: 'Mendoj (nedevige)',
    tone: 'optional',
    steps: [
      {
        text: 'En la Dua Bulteno vi trovas la mendeblajn servojn: loĝado, ekskursoj, bankedo, antaŭ- kaj postkongresoj.',
        width: 2.8,
      },
      { text: 'Se vi volas, vi mendas kaj pagas la elektitajn servojn.', width: 1.6 },
      { text: 'UEA konfirmas viajn mendojn.', width: 1.1 },
    ],
  },
  { title: '', tone: 'main', end: true, steps: [{ text: 'Universala Kongreso', width: 1 }] },
];

// Larĝoj de la kolumnoj ĉe la horizontala aranĝo: proporciaj al la longo de la tekstoj.
// Ĉe ŝanĝo de teksto reĝustigu "width".
const allSteps = phases.flatMap((ph) => ph.steps.map((s) => ({ ...s, tone: ph.tone, end: !!ph.end })));
const gridColumns = allSteps.map((s) => `minmax(0, ${s.width}fr)`).join(' ');

let col = 1;
const phaseSpans = phases.map((ph) => {
  const span = { title: ph.title, tone: ph.tone, start: col, end: col + ph.steps.length };
  col += ph.steps.length;
  return span;
});
</script>

<template>
  <div class="kt-tl" role="group" aria-labelledby="kt-h-tl">
    <h3 id="kt-h-tl" class="kt-tl__title">Kiel okazas la aliĝo</h3>

    <!-- Horizontala aranĝo (de 1000 px) -->
    <div class="kt-tl__h" :style="{ gridTemplateColumns: gridColumns }" aria-hidden="false">
      <div
        v-for="ph in phaseSpans.filter((p) => p.title)"
        :key="ph.title"
        class="kt-tl__phase"
        :class="`kt-tl__phase--${ph.tone}`"
        :style="{ gridColumn: `${ph.start} / ${ph.end}` }"
      >
        {{ ph.title }}
      </div>

      <div
        v-for="(s, i) in allSteps"
        :key="'n' + i"
        class="kt-tl__node"
        :class="[`kt-tl__node--${s.tone}`, { 'kt-tl__node--end': s.end, 'kt-tl__node--first': i === 0 }]"
      ></div>

      <div v-for="(s, i) in allSteps" :key="'t' + i" class="kt-tl__text" :class="{ 'kt-tl__text--end': s.end }">
        {{ s.text }}
      </div>
    </div>

    <!-- Vertikala aranĝo (sub 1000 px) -->
    <ol class="kt-tl__v">
      <template v-for="(ph, pi) in phases" :key="pi">
        <li v-if="ph.title" class="kt-tl__vphase" :class="`kt-tl__v--${ph.tone}`">{{ ph.title }}</li>
        <li
          v-for="s in ph.steps"
          :key="s.text"
          class="kt-tl__vstep"
          :class="[`kt-tl__v--${ph.tone}`, { 'kt-tl__vstep--end': ph.end }]"
        >
          {{ s.text }}
        </li>
      </template>
    </ol>
  </div>
</template>
