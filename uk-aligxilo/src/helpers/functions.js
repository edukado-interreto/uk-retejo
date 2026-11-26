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

/**
 * ID of the registration in the booking form URL, or null if missing.
 * Works on every page whose slug starts with "mendilo": `/mendilo/<id>`, `/mendilo-sekreta/<id>`…
 */
export function registrationIdFromUrl() {
  const match = /\/mendilo[\w-]*\/(?<id>\w+)/.exec(window.location.pathname);
  return match === null ? null : match.groups.id;
}
