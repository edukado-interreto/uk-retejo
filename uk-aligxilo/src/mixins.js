export default {
  methods: {
    flagEmoji(countryCode) {
      const codePoints = countryCode
        .substring(0, 2)
        .toUpperCase()
        .split("")
        .map((char) => 127397 + char.charCodeAt())
      return String.fromCodePoint(...codePoints)
    },
    scrollTo(id, pixels = 32) {
      this.$nextTick(() => {
        console.log("scrolling to #" + id)
        const element = document.getElementById(id)
        if (element !== null) {
          const top = element.getBoundingClientRect().top + window.scrollY - pixels
          window.scrollTo({
            top,
            left: 0,
            behavior: "smooth",
          })
        }
      })
    },
    /**
     * Takes an int and returns a string like "10:30"
     * @param min
     */
    minutesToTime(min) {
      const hours = Math.floor(min / 60).toString()
      const minutes = (min % 60).toString()
      return `${hours.padStart(2, "0")}:${minutes.padStart(2, "0")}`
    },
    formatDate(date, n = false, year = false) {
      const elements = date.split("-")
      const months = [
        "",
        "januaro",
        "februaro",
        "marto",
        "aprilo",
        "majo",
        "junio",
        "julio",
        "aŭgusto",
        "septembro",
        "oktobro",
        "novembro",
        "decembro",
      ]
      let dateString = `${parseInt(elements[2])}-a${n ? "n" : ""} de ${months[parseInt(elements[1])]}`
      if (year) {
        dateString += " " + elements[0]
      }
      return dateString
    },
  },
}
