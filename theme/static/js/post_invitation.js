document.getElementById("rsvp-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const confirmacao = formData.getAll("confirmacao");
  const codigo_acesso = formData.get("codigo_acesso");

  fetch("/api/confirmar/" + codigo_acesso + "/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      confirmacao: confirmacao,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("form-container").classList.add("hidden");
        document.getElementById("success-container").classList.remove("hidden");
        
        document.getElementById("success-container").scrollIntoView({ behavior: 'smooth' });
      } else {
        alert("Erro: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocorreu um erro ao enviar a confirmação.");
    });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}