const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("navbar-menu");

navToggle.addEventListener("click", () => {
  navMenu.classList.toggle("hidden");
});

navMenu.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    if (!navMenu.classList.contains("hidden")) {
      navMenu.classList.add("hidden");
    }
  });
});
