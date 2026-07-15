<template>
  <n-layout id="layout">
    <n-layout-header id="page-header" is="header" class="framed">
      <router-link :to="{ name: 'registrationForm' }">
        <img src="/img/emblemo_uea.png" alt="Universala Esperanto-Asocio" />
      </router-link>
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

    <n-layout-content id="uk-footer" class="framed">
      <n-flex style="align-items: center" justify="space-between">
        <n-flex :size="28" style="align-items: center" id="footer-logos">
          <a v-for="logo in logos" :key="logo.src" :href="logo.url" :title="logo.alt" target="_blank">
            <img :src="logo.src" :alt="logo.alt" loading="lazy" :style="{ height: logo.height + 'px' }" />
          </a>
        </n-flex>
        <div id="footer-contact">
          <div id="footer-email">
            <a href="mailto:kongresoj@co.uea.org">
              <n-icon size="22"><EmailIcon /></n-icon>
              kongresoj@co.uea.org
            </a>
          </div>
          <div id="footer-social">
            <a href="https://uk.telegramo.org/" target="_blank" title="Telegram">
              <n-icon size="28"><TelegramIcon /></n-icon>
            </a>
            <a href="https://www.instagram.com/universala.kongreso/" target="_blank" title="Instagram">
              <n-icon size="28"><InstagramIcon /></n-icon>
            </a>
            <a href="https://www.facebook.com/universala.kongreso/" target="_blank" title="Facebook">
              <n-icon size="28"><FacebookIcon /></n-icon>
            </a>
          </div>
        </div>
      </n-flex>
    </n-layout-content>
  </n-layout>
</template>

<script setup>
import SideMenu from './SideMenu.vue';
import { NIcon, NFlex } from 'naive-ui';
import FacebookIcon from '../ui/icons/FacebookIcon.vue';
import InstagramIcon from '../ui/icons/InstagramIcon.vue';
import EmailIcon from '../ui/icons/EmailIcon.vue';
import TelegramIcon from '../ui/icons/TelegramIcon.vue';

const logos = [
  {
    src: '/img/uea.png',
    alt: 'Universala Esperanto-Asocio',
    url: 'https://uea.org/',
    height: 84,
  },
  {
    src: '/img/partners/unesco.png',
    alt: 'Immaterielles Kulturerbe in Österreich',
    url: 'https://www.unesco.at/kultur/immaterielles-kulturerbe',
    height: 70,
  },
  {
    src: '/img/partners/region_graz.png',
    alt: 'Region Graz',
    url: 'https://www.regiongraz.at/',
  },
  {
    src: '/img/partners/graz_convention.png',
    alt: 'Graz Convention Bureau',
    url: 'https://www.graztourismus.at/kongress/',
  },
  {
    src: '/img/partners/aef.png',
    alt: 'Aŭstria Esperanto-Federacio',
    url: 'https://www.esperanto.at/',
  },
  {
    src: '/img/partners/eo-stirio.png',
    alt: 'Esperanto-Societo Stirio',
    url: 'https://www.esperanto-graz.at/',
    height: 60,
  },
];
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

#uk-footer {
  margin-bottom: 0.4em;
  padding: 0.7rem;
}

#footer-logos img {
  height: 50px;
  transition-property: opacity;
  transition-duration: 0.2s;
}

#footer-logos a:hover img {
  opacity: 0.8;
}

#footer-contact a:link,
#footer-contact a:visited {
  color: #333;
  text-decoration: none;
}

#footer-contact a:hover,
#footer-contact a:focus {
  color: #000;
}

#footer-email {
  margin-bottom: 0.5rem;
  font-size: 18px;
}

#footer-email a {
  display: flex;
  align-items: center;
  gap: 5px;
}

#footer-social {
  text-align: right;
}

#footer-social a + a {
  margin-left: 4px;
}
</style>
