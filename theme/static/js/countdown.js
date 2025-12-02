// Countdown
const weddingTime = new Date(2026, 10, 22, 10, 0, 0).getTime();
const elDias = document.getElementById("dias");
const elHoras = document.getElementById("horas");
const elMinutos = document.getElementById("minutos");
const elSegundos = document.getElementById("segundos");
const pad = (value, length = 2) => String(value).padStart(length, "0");

function updateCountdown() {
  const now = Date.now();
  const distance = weddingTime - now;

  if (distance <= 0) {
    elDias.textContent = "0";
    elHoras.textContent = "00";
    elMinutos.textContent = "00";
    elSegundos.textContent = "00";
    clearInterval(countdownInterval);
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
const countdownInterval = setInterval(updateCountdown, 1000);
