<script setup>
import { computed, h } from 'vue';
import { NDataTable } from 'naive-ui';
import { PRICE_ROWS } from './useKotizoj';

const props = defineProps({
  periods: { type: Array, required: true },
  nowIndex: { type: Number, required: true },
  category: { type: String, default: null }, // 'A', 'B' aŭ null
  texts: { type: Object, required: true },
  price: { type: Function, required: true },
});

const rows = computed(() => [
  ...PRICE_ROWS.map((r) => ({ ...r, sub: r.withSub ? props.texts.rabataj : null })),
  { key: 'free', free: true, label: props.texts.senpagaj },
]);

function periodClass(i) {
  if (i < props.nowIndex) return 'kt-past';
  if (i === props.nowIndex) return 'kt-now';
  return 'kt-future';
}

const columns = computed(() => [
  {
    key: 'group',
    title: () => h('span', { class: 'kt-sr' }, 'Kategorio'),
    className: 'kt-col-group',
    width: 230,
    rowSpan: (row) => (row.groupFirst ? 2 : 1),
    colSpan: (row) => (row.free ? 2 : 1),
    render: (row) =>
      row.free
        ? h('span', { class: 'kt-free-label' }, row.label)
        : h('div', [
            h('div', { class: 'kt-group' }, row.group),
            row.sub ? h('div', { class: 'kt-group-sub' }, row.sub) : null,
          ]),
  },
  {
    key: 'label',
    title: () => h('span', { class: 'kt-sr' }, 'Membreco'),
    className: 'kt-col-label',
    width: 150,
    render: (row) => row.label,
  },
  ...props.periods.map((p, i) => ({
    key: `p${i}`,
    align: 'center',
    className: periodClass(i),
    // Ĉiuj kaplinioj rezervas spacon por la insigno, por ke la datoj staru sur la sama linio.
    title: () =>
      h('div', { class: 'kt-ph' }, [
        h('div', { class: 'kt-ph__badge' }, i === props.nowIndex ? h('span', { class: 'kt-badge' }, 'Nun') : null),
        h('div', { class: 'kt-ph__date' }, p.label),
        h('div', { class: 'kt-ph__sub' }, p.sub),
      ]),
    children: ['A', 'B'].map((cat) => ({
      key: `p${i}${cat}`,
      title: cat,
      align: 'center',
      minWidth: 76,
      className: [periodClass(i), i === props.nowIndex && cat === props.category ? 'kt-mine' : ''].join(' '),
      render: (row) => `${props.price(cat, row.key, i)} €`,
    })),
  })),
]);
</script>

<template>
  <div class="kt-table">
    <n-data-table
      :columns="columns"
      :data="rows"
      :row-key="(row) => row.key"
      :single-line="false"
      :bordered="true"
      :scroll-x="1000"
      size="medium"
    />
  </div>
</template>
