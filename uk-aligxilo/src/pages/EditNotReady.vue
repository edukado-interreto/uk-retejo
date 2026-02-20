<template>
  <n-h2>Mendilo</n-h2>
  <n-alert title="La mendilo ankoraŭ ne funkcias" type="error">
    La mendilo ankoraŭ ne funkcias. Ni sciigos vin per retmesaĝo, kiam ĝi ekfunkcios.
  </n-alert>
</template>

<script>
export default {
  name: "EditNotReady",
}
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 10vh;
  margin-bottom: 10vh;
  transform: scale(3);
}
</style>