const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("navbar-menu");

if (navToggle && navMenu) {
  navToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    const isExpanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isExpanded));
    navMenu.classList.toggle("hidden");
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (!navMenu.classList.contains("hidden")) {
        navMenu.classList.add("hidden");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("click", (event) => {
    if (
      !navMenu.classList.contains("hidden") &&
      !navMenu.contains(event.target) &&
      !navToggle.contains(event.target)
    ) {
      navMenu.classList.add("hidden");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
}
