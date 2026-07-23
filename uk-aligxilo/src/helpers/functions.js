import { nextTick } from 'vue';

export const scrollTo = (id, pixels = 32) => {
  nextTick(() => {
    const element = document.getElementById(id);
    if (element !== null) {
      const top = element.getBoundingClientRect().top + window.scrollY - pixels;
      window.scrollTo({
        top,
        left: 0,
        behavior: 'smooth',
      });
    }
  });
};

export function flagEmoji(countryCode) {
  const codePoints = countryCode
    .substring(0, 2)
    .toUpperCase()
    .split('')
    .map((char) => 127397 + char.charCodeAt());
  return String.fromCodePoint(...codePoints);
}
