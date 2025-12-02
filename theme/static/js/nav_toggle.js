// Mobile Menu Toggle
const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("navbar-menu");

navToggle.addEventListener("click", () => {
  navMenu.classList.toggle("hidden");
});

// Close menu when clicking a link
navMenu.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    if (!navMenu.classList.contains("hidden")) {
      navMenu.classList.add("hidden");
    }
  });
});
