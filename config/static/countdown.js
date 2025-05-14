document.addEventListener("DOMContentLoaded", () => {
  ///////////////
  // Countdown //
  ///////////////
  const countdown = document.querySelector(".event-countdown")
  const start = new Date(countdown.dataset.countdown)

  const weeks = countdown.querySelector(".weeks")
  const days = countdown.querySelector(".days")
  const hours = countdown.querySelector(".hours")
  const minutes = countdown.querySelector(".minutes")
  const seconds = countdown.querySelector(".seconds")

  /**
   * Updates the inner HTML of an element if it differs from the provided value.
   * This function helps optimize DOM manipulation by only updating when necessary.
   *
   * @param {HTMLElement} el - The DOM element to update
   * @param {number} val - The numeric value to set as the element's inner HTML
   * @returns {void}
   *
   * @example
   * // Updates the element's innerHTML to "42" only if it's not already "42"
   * const counterElement = document.getElementById('counter');
   * apply(counterElement, 42);
   */
  const apply = (el, val) => {
    const value = Math.floor(val).toString()
    if (el.innerHTML !== value) el.innerHTML = value
  }

  const updateCountdown = () => {
    const sec = Math.floor((start - new Date()) / 1000)

    apply(weeks, sec / (60 * 60 * 24 * 7))
    apply(days, (sec / (60 * 60 * 24)) % 7)
    apply(hours, (sec / (60 * 60)) % 24)
    apply(minutes, (sec / 60) % 60)
    apply(seconds, sec % 60)
  }
  setInterval(updateCountdown, 1000)
})
