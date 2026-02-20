<template>
  <n-grid x-gap="20" :cols="4" style="margin-bottom: 2rem">
    <n-grid-item span="3">
      <n-h1>111-a Universala Kongreso de Esperanto</n-h1>
      <div class="subheader">Graz — Aŭstrio</div>
      <div class="dates">1-a — 8-a de aŭgusto 2026</div>
    </n-grid-item>
    <n-grid-item>
      <img src="/img/graz2026.png" alt="Graz 2026" class="logo" />
    </n-grid-item>
  </n-grid>
</template>

<script>
export default {
  name: 'CongressHeader',
};
</script>

<style scoped>
h1 {
  background: #e9f3fc;
  padding: 10px;
}

.logo {
  display: block;
  margin: auto;
}

.subheader {
  font-size: 1.4rem;
  margin-top: 1rem;
}

.dates {
  font-size: 1.1rem;
  color: #ff6633;
  margin-top: 1rem;
}

@media only screen and (max-width: 600px) {
  h1 {
    font-size: 1.4em;
    padding: 6px;
  }
}
</style>
