<template>
  <n-layout id="layout">
    <n-layout-header id="page-header" is="header" class="framed">
      <router-link :to="{ name: 'registrationForm' }"
        ><img src="/img/emblemo_uea.png" alt="Universala Esperanto-Asocio"
      /></router-link>
    </n-layout-header>

    <n-layout-content id="main-content" class="framed">
      <n-grid x-gap="16" y-gap="12" :cols="11" item-responsive responsive="screen">
        <n-grid-item span="11 m:2">
          <side-menu />
        </n-grid-item>
        <n-grid-item span="11 m:9" class="main-grid">
          <router-view></router-view>
        </n-grid-item>
      </n-grid>
    </n-layout-content>
  </n-layout>
</template>

<script setup>
import SideMenu from './SideMenu.vue';
</script>

<style>
html {
  height: 100%;
}

body {
  margin: 0;
  padding: 0 0.5rem;
  background: rgb(233, 243, 252)
    linear-gradient(180deg, rgba(233, 243, 252, 1) 0, rgba(203, 230, 248, 1) 250px, rgba(233, 243, 252, 1) 500px)
    no-repeat;
}

img {
  max-width: 100%;
  height: auto;
}

#layout {
  max-width: 1300px;
  margin: 1rem auto auto;
}

#page-header {
  margin-bottom: 0.5rem;
  padding: 0.4rem 0.1rem;
}

.framed {
  border: 1px solid #25aae1;
  background: white;
  border-radius: 5px;
}

#main-content {
  margin: 1rem 0;
  padding: 1rem;
}

.main-grid {
  padding-top: 0.55rem;
}
</style>
