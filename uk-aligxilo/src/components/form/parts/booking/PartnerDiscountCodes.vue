<template>
  <n-p>Kiel aliĝinto vi ricevas rabaton ĉe la partneroj de la kongreso.</n-p>
  <n-p><strong>Bonvolu ne diskonigi la kodojn: ili estas nur por kongresanoj.</strong></n-p>

  <n-card :segmented="{ action: true }">
    <template v-for="(partner, index) in partners" :key="partner.name">
      <n-divider v-if="index > 0" />
      <n-flex align="center" justify="space-between" :size="[24, 12]">
        <n-flex align="center" :size="24" :wrap="false">
          <img :src="partner.logo" :alt="partner.name" width="140" />
          <div class="partner-title">{{ partner.title }}</div>
        </n-flex>
        <div class="code-row">
          <span class="code">{{ partner.code }}</span>
          <n-button
            type="primary"
            size="large"
            :ghost="copiedCode !== partner.code"
            :aria-label="`Kopii la ${partner.name}-kodon`"
            @click="copy(partner.code)"
          >
            <template #icon>
              <n-icon>
                <IconCheck v-if="copiedCode === partner.code" />
                <IconCopy v-else />
              </n-icon>
            </template>
            <span aria-live="polite">{{ copiedCode === partner.code ? 'Kopiita' : 'Kopii' }}</span>
          </n-button>
        </div>
      </n-flex>
    </template>

    <template #action>
      <n-flex align="center" justify="space-between" :size="[24, 12]">
        <n-flex :wrap="false" :size="8">
          <n-text type="warning">
            <n-icon size="18"><IconAlertTriangle /></n-icon>
          </n-text>
          <n-text depth="2">
            <n-text type="warning" strong>
              La Qantas-kodo funkcias nur, se vi iras al Qantas per la ligilo en la paĝo Alvenebloj.
            </n-text>
            Tie troviĝas ankaŭ ĉiuj detaloj pri la rabatoj.
          </n-text>
        </n-flex>
        <n-button
          class="alvenebloj-link"
          tag="a"
          type="primary"
          size="large"
          icon-placement="right"
          :href="alveneblojUrl"
          target="_blank"
          rel="noopener"
        >
          <template #icon>
            <n-icon><IconExternalLink /></n-icon>
          </template>
          Malfermi la paĝon Alvenebloj
        </n-button>
      </n-flex>
    </template>
  </n-card>
</template>

<script setup>
import { computed } from 'vue';
import { useClipboard } from '@vueuse/core';
import { NDivider, NFlex, NIcon, NText } from 'naive-ui';
import { IconAlertTriangle, IconCheck, IconCopy, IconExternalLink } from '@tabler/icons-vue';
import qantasLogo from '@/assets/partneroj/qantas.png';
import skybusLogo from '@/assets/partneroj/skybus.png';

// La Qantas-rabato validas nur, se oni venas al Qantas de la paĝo Alvenebloj:
// do neniam ligu rekte al Qantas el la mendilo.
const alveneblojUrl = import.meta.env.VITE_WEBSITE_URL + '/alvenebloj';

const partners = [
  { name: 'Qantas', title: 'Flugbiletoj', code: '202521', logo: qantasLogo },
  { name: 'SkyBus', title: 'Busbiletoj', code: 'WCUEA27', logo: skybusLogo },
];

const { copy, copied, text } = useClipboard({ copiedDuring: 2000, legacy: true });

const copiedCode = computed(() => (copied.value ? text.value : null));
</script>

<style scoped>
.partner-title {
  font-family: var(--font-title);
  font-weight: 600;
  font-size: 18px;
  line-height: 1.3;
  color: #1e2939;
}

.code-row {
  display: flex;
  gap: 8px;
  flex: 1 1 280px;
  max-width: 336px;
}

@media (max-width: 600px) {
  .code-row {
    max-width: none;
  }
}

.code {
  flex: 1;
  min-width: 0;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  padding: 0 14px;
  border: 1.5px dashed #99a1af;
  border-radius: 6px;
  background: #f9fafb;
  font-family: ui-monospace, 'JetBrains Mono', Consolas, monospace;
  font-weight: 600;
  font-size: 16px;
  letter-spacing: 0.05em;
  color: #1e2939;
  user-select: all;
  overflow-wrap: anywhere;
}

/* Sen tio la stiloj de .prose (ligiloj) kolorigas la tekston verde sur la verda butono. */
.alvenebloj-link,
.alvenebloj-link:hover {
  color: #fff;
  text-decoration: none;
}
</style>
