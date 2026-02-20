<template>
  <n-breadcrumb style="margin-bottom: 1rem;">
    <n-breadcrumb-item>
      <router-link :to="{ name: 'admin' }">
        Adminejo
      </router-link>
    </n-breadcrumb-item>
    <n-breadcrumb-item>
      {{title }}
    </n-breadcrumb-item>
  </n-breadcrumb>
</template>

<script>
import {NBreadcrumb, NBreadcrumbItem} from "naive-ui";

export default {
  name: "AdminBreadcrumbs",
  components: {NBreadcrumbItem, NBreadcrumb},
  props: {
    title: String
  }
}
</script>

<style scoped>

</style>