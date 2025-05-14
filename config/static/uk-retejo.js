document.addEventListener("DOMContentLoaded", () => {
  //////////////
  // Navigation
  //////////////
  const navbar = document.getElementById("navbar")

  // Function to handle the scroll event
  function handleScroll() {
    if (window.scrollY > 50) {
      navbar.classList.add("bg-base-100", "shadow-md") // Add background and shadow
      navbar.classList.remove("bg-opacity-0", "dark") // Remove transparent background
    } else {
      navbar.classList.add("bg-opacity-0", "dark") // Make transparent
      navbar.classList.remove("bg-base-100", "shadow-md") // Remove background and shadow
    }
  }

  // Initial check in case the page loads already scrolled
  handleScroll()

  // Listen for the scroll event
  window.addEventListener("scroll", handleScroll)
})
