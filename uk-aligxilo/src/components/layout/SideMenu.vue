<template>
  <ul>
    <li>
      <a href="https://uea.org/" target="_blank">
        Retejo de UEA
        <n-icon size="18">
          <ExternalLinkIcon />
        </n-icon>
      </a>
    </li>
    <li>
      <router-link :to="{ name: 'registrationForm' }">Aliĝi al UK 2026</router-link>
    </li>
    <li>
      <router-link :to="{ name: 'registeredParticipants' }">Listo de aliĝintoj</router-link>
    </li>
    <li>
      <router-link :to="{ name: 'pricetable' }">Kotiztabelo</router-link>
    </li>
    <!--    <li>-->
    <!--      <router-link :to="{ name: 'program' }">-->
    <!--        Programo-->
    <!--      </router-link>-->
    <!--    </li>-->
    <li>
      <router-link :to="{ name: 'unuaBulteno' }">Unua Bulteno</router-link>
    </li>
    <!-- <li>
      <router-link :to="{ name: 'duaBulteno' }"> Dua Bulteno </router-link>
    </li> -->
    <!-- <li>
      <a href="https://iik.uea.org/2026/" target="_blank">
        Infana Kongreseto (IIK)
        <n-icon size="18"> <ExternalLinkIcon /> </n-icon>
      </a>
    </li> -->
    <!--    <li>-->
    <!--      <router-link :to="{ name: 'congressBook' }">-->
    <!--        Kongresa libro-->
    <!--      </router-link>-->
    <!--    </li>-->
    <li>
      <a href="https://mallonge.net/UK26proponuprogrameron" target="_blank">
        Proponu programeron
        <n-icon size="18">
          <ExternalLinkIcon />
        </n-icon>
      </a>
    </li>
    <!-- <li>
      <a href="https://forms.gle/Aoyrw4yLVeAP58mr9" target="_blank">
        Salonmendilo
        <n-icon size="18">
          <ExternalLinkIcon />
        </n-icon>
      </a>
    </li> -->
    <li>
      <a href="https://www.graztourismus.at/Prospekte/PDFs/sights-of-graz-esperanto-2025.pdf" target="_blank">
        Broŝuro pri Graz
        <n-icon size="18">
          <ExternalLinkIcon />
        </n-icon>
      </a>
    </li>
  </ul>
</template>

<script setup>
import { NIcon } from 'naive-ui';
import ExternalLinkIcon from '@/components/ui/icons/ExternalLinkIcon.vue';
</script>

<style scoped lang="scss">
i.n-icon {
  transform: translateY(2px);
}

ul {
  padding: 0;
  margin: 0;
  list-style-type: none;
}

li {
  margin: 0;
  margin-top: 0.5rem;
}

a {
  display: block;
  margin-right: 8px;
  padding: 12px 10px;
  color: #111;
  font-size: 1.1em;
  background-color: #e9f3fc;
  border: 1px solid #99ccff;
  border-radius: 4px;
  text-decoration: none;

  &:hover,
  &:focus,
  &:active,
  &.router-link-active {
    color: #000;
    background-color: #99ccff;
  }

  &.router-link-active {
    font-weight: 600;
  }
}

@media screen and (max-width: 1024px) {
  ul {
    text-align: center;
  }

  li {
    display: inline-block;
    margin: 0.3rem;
  }

  a {
    display: inline-block;
    font-size: 1em;
  }
}

@media only screen and (max-width: 600px) {
  a {
    margin-right: 0;
    padding: 5px 6px;
    border-radius: 3px;
  }
}
</style>
