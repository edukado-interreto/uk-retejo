import { computed, onBeforeUnmount, ref, toValue } from 'vue';

const MONATOJ = [
  'januaro',
  'februaro',
  'marto',
  'aprilo',
  'majo',
  'junio',
  'julio',
  'aŭgusto',
  'septembro',
  'oktobro',
  'novembro',
  'decembro',
];
const MONATOJ_MALLONGE = [
  'jan.',
  'feb.',
  'mar.',
  'apr.',
  'maj.',
  'jun.',
  'jul.',
  'aŭg.',
  'sep.',
  'okt.',
  'nov.',
  'dec.',
];

function parts(iso) {
  const [y, m, d] = iso.split('-').map(Number);
  return { y, m, d };
}

function dayAfter(iso) {
  const { y, m, d } = parts(iso);
  const next = new Date(Date.UTC(y, m - 1, d + 1));
  return next.toISOString().slice(0, 10);
}

export function shortDate(iso) {
  const { y, m, d } = parts(iso);
  return `${d} ${MONATOJ_MALLONGE[m - 1]} ${y}`;
}

export function longDate(iso) {
  const { y, m, d } = parts(iso);
  return `la ${d}-a de ${MONATOJ[m - 1]} ${y}`;
}

/** Serĉo sen supersignoj kaj kun x-sistemo: "cinio", "cxinio" kaj "ĉinio" ĉiuj trovas "Ĉinio". */
export function normalize(text) {
  return text
    .toLowerCase()
    .replace(/cx/g, 'c')
    .replace(/gx/g, 'g')
    .replace(/hx/g, 'h')
    .replace(/jx/g, 'j')
    .replace(/sx/g, 's')
    .replace(/ux/g, 'u')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

export function useMediaQuery(query) {
  const mql = typeof window !== 'undefined' ? window.matchMedia(query) : null;
  const matches = ref(mql ? mql.matches : false);
  const onChange = (e) => {
    matches.value = e.matches;
  };
  if (mql) mql.addEventListener('change', onChange);
  onBeforeUnmount(() => {
    if (mql) mql.removeEventListener('change', onChange);
  });
  return matches;
}

/**
 * @param dataSource  ref aŭ getter kun la datumoj (vidu PriceTable.vue en src/pages)
 * @param currentPeriod ref aŭ getter kun la indekso de la nuna periodo, kalkulita de la servilo
 * @param country ref kun la oficiala nomo de la lando aŭ null
 */
export function useKotizoj(dataSource, currentPeriod, country) {
  const data = computed(() => toValue(dataSource));

  const periods = computed(() =>
    data.value.periodoj.map((p, i) => {
      const start = i > 0 ? dayAfter(data.value.periodoj[i - 1].gxis) : null;
      return {
        numero: p.numero,
        gxis: p.gxis,
        label: p.gxis ? `ĝis ${shortDate(p.gxis)}` : `ekde ${shortDate(start)}`,
        longLabel: p.gxis ? `ĝis ${longDate(p.gxis)}` : `ekde ${longDate(start)}`,
        sub: `${p.numero}-a aliĝperiodo`,
      };
    }),
  );

  const nowIndex = computed(() => {
    const last = data.value.periodoj.length - 1;
    const i = toValue(currentPeriod);
    return Number.isInteger(i) ? Math.min(Math.max(i, 0), last) : last;
  });

  const category = computed(() => {
    if (!country.value) return null;
    if (data.value.landoj_A.includes(country.value)) return 'A';
    if (data.value.landoj_B.includes(country.value)) return 'B';
    return null;
  });

  const countryOptions = computed(() =>
    [...data.value.landoj_A, ...data.value.landoj_B]
      .sort((a, b) => a.localeCompare(b, 'eo'))
      .map((name) => {
        const flag = data.value.flagoj?.[name];
        return { label: flag ? `${flag} ${name}` : name, value: name };
      }),
  );

  const youthFrom = computed(() => data.value.junulo.de.slice(0, 4));
  const youthTo = computed(() => data.value.junulo.gxis.slice(0, 4));
  const freeAfterYear = computed(() => data.value.senpage_post.slice(0, 4));

  const texts = computed(() => ({
    rabataj: `junuloj (naskiĝintaj ${youthFrom.value}-${youthTo.value}), samadresaj kunuloj, handikapuloj, komitatanoj`,
    senpagaj: `Infanoj kaj adoleskuloj (naskiĝintaj post ${freeAfterYear.value}) kaj nemalhaveblaj akompanantoj de handikapuloj`,
  }));

  const price = (cat, key, i) => (key === 'free' ? 0 : data.value.prezoj[cat][key][i]);

  return { periods, nowIndex, category, countryOptions, texts, price };
}

/** La vicoj de la tabelo, en la sama ordo ĉe komputilo kaj telefono. */
export const PRICE_ROWS = [
  { key: 'membro', group: 'Plena kotizo', groupFirst: true, label: 'Membro de UEA' },
  { key: 'nemembro', group: 'Plena kotizo', label: 'Nemembro' },
  { key: 'membro_rabatita', group: 'Rabatita kotizo', groupFirst: true, withSub: true, label: 'Membro de UEA' },
  { key: 'nemembro_rabatita', group: 'Rabatita kotizo', label: 'Nemembro' },
];
