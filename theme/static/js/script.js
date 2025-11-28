const dataCasamento = new Date(2026, 10, 22, 10, 0, 0).getTime();

const intervalo = setInterval(function () {
  const agora = new Date().getTime();

  const distancia = dataCasamento - agora;

  const dias = Math.floor(distancia / (1000 * 60 * 60 * 24));
  const horas = Math.floor(
    (distancia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
  );
  const minutos = Math.floor((distancia % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((distancia % (1000 * 60)) / 1000);

  document.getElementById("dias").innerText = dias;
  document.getElementById("horas").innerText = horas;
  document.getElementById("minutos").innerText = minutos;
  document.getElementById("segundos").innerText = segundos;

  if (distancia < 0) {
    clearInterval(intervalo);
    document.getElementById("dias").innerText = "0";
    document.getElementById("horas").innerText = "0";
    document.getElementById("minutos").innerText = "0";
    document.getElementById("segundos").innerText = "0";
  }
}, 1000);
