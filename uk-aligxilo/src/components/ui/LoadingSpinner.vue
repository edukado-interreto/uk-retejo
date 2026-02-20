<template>
  <div
      class="loading"
  >
    <n-spin size="large" />
  </div>
</template>

<script>
export default {
  name: "LoadingSpinner"
}
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 20vh;
  margin-bottom: 20vh;
  transform: scale(3);
}
</style>