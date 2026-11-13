<script setup>
import { NCollapse, NCollapseItem } from 'naive-ui';
import { PRICE_ROWS } from './useKotizoj';

const props = defineProps({
  periods: { type: Array, required: true },
  nowIndex: { type: Number, required: true },
  category: { type: String, default: null },
  texts: { type: Object, required: true },
  price: { type: Function, required: true },
});

const groups = [
  { title: 'Plena kotizo', rows: PRICE_ROWS.slice(0, 2), withSub: false },
  { title: 'Rabatita kotizo', rows: PRICE_ROWS.slice(2, 4), withSub: true },
];

const cellClass = (i, cat) => (i === props.nowIndex && cat === props.category ? 'kt-mine' : '');
</script>

<template>
  <n-collapse class="kt-cards" :default-expanded-names="[`p${nowIndex}`]" display-directive="show">
    <n-collapse-item
      v-for="(p, i) in periods"
      :key="p.numero"
      :name="`p${i}`"
      :class="['kt-card', { 'kt-card--now': i === nowIndex, 'kt-card--past': i < nowIndex }]"
    >
      <template #header>
        <div class="kt-card__head">
          <span class="kt-card__date">{{ p.label }}</span>
          <span class="kt-card__sub">{{ p.sub }}</span>
        </div>
      </template>
      <template #header-extra>
        <span v-if="i === nowIndex" class="kt-badge">Nun</span>
      </template>

      <table class="kt-mini">
        <thead>
          <tr>
            <th scope="col"><span class="kt-sr">Kategorio</span></th>
            <th scope="col" :class="cellClass(i, 'A')">A</th>
            <th scope="col" :class="cellClass(i, 'B')">B</th>
          </tr>
        </thead>
        <tbody v-for="g in groups" :key="g.title">
          <tr class="kt-mini__group">
            <th scope="rowgroup" colspan="3">
              {{ g.title }}
              <div v-if="g.withSub" class="kt-mini__sub">{{ texts.rabataj }}</div>
            </th>
          </tr>
          <tr v-for="r in g.rows" :key="r.key">
            <th scope="row">{{ r.label }}</th>
            <td :class="cellClass(i, 'A')">{{ price('A', r.key, i) }} €</td>
            <td :class="cellClass(i, 'B')">{{ price('B', r.key, i) }} €</td>
          </tr>
        </tbody>
      </table>

      <div class="kt-mini__free">
        <span>{{ texts.senpagaj }}</span>
        <strong>0 €</strong>
      </div>
    </n-collapse-item>
  </n-collapse>
</template>
