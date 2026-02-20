export const formatTime = (dateObj) =>
  dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });

export const formatDateString = (date, n = false, year = false) => {
  const elements = date.split('-');
  const months = [
    '',
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
  let dateString = `${parseInt(elements[2])}-a${n ? 'n' : ''} de ${months[parseInt(elements[1])]}`;
  if (year) {
    dateString += ' ' + elements[0];
  }
  return dateString;
};

export const dayOfWeekEO = (date, capitalize = false) => {
  const dateObj = new Date(date);
  const day = dateObj.getUTCDay();
  const days = ['dimanĉo', 'lundo', 'mardo', 'merkredo', 'ĵaŭdo', 'vendredo', 'sabato'];
  if (capitalize) {
    return days[day].charAt(0).toUpperCase() + days[day].slice(1);
  }
  return days[day];
};
