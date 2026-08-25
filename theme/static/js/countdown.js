function initCountdown() {
  const container = document.getElementById("countdown-container");
  if (!container) return;
  const rawDate = container.getAttribute("data-date");
  if (!rawDate) return;

  // Ensure parsing across browsers by standardizing format or relying on ISO
  let parsedDate = new Date(rawDate);
  if (isNaN(parsedDate.getTime())) {
    parsedDate = new Date(rawDate.replace(/-/g, '/').replace('T', ' '));
  }

  const weddingTime = parsedDate.getTime();
  if (isNaN(weddingTime)) {
    console.error("Invalid countdown date:", rawDate);
    return;
  }
  const elDias = document.getElementById("dias");
  const elHoras = document.getElementById("horas");
  const elMinutos = document.getElementById("minutos");
  const elSegundos = document.getElementById("segundos");

  if (!elDias || !elHoras || !elMinutos || !elSegundos) return;

  const pad = (value, length = 2) => String(value).padStart(length, "0");
  let intervalId = null;

  function updateCountdown() {
    const now = Date.now();
    const distance = weddingTime - now;

    if (distance <= 0) {
      elDias.textContent = "0";
      elHoras.textContent = "00";
      elMinutos.textContent = "00";
      elSegundos.textContent = "00";
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    elDias.textContent = String(days);
    elHoras.textContent = pad(hours);
    elMinutos.textContent = pad(minutes);
    elSegundos.textContent = pad(seconds);
  }

  updateCountdown();
  intervalId = setInterval(updateCountdown, 1000);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initCountdown);
} else {
  initCountdown();
}
