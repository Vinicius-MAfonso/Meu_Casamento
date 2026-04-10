document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("rsvp-form");
  if (!form) return;
  
  if (form.dataset.listenerAttached) return;
  form.dataset.listenerAttached = 'true';
  
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = 'Enviando...';
    
    const checkedBoxes = document.querySelectorAll(
      'input[name="confirmacao"]:checked'
    );

    if (checkedBoxes.length === 0) {
      submitButton.disabled = false;
      submitButton.textContent = 'Confirmar Presença';
      return showToast("Por favor, selecione pelo menos um convidado para confirmar presença.", "warning");
    }

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
          showToast("Presença confirmada com sucesso!", "success");
          confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
          });
          document.getElementById("form-container").classList.add("hidden");
          document.getElementById("success-container").classList.remove("hidden");
          
          document.getElementById("success-container").scrollIntoView({ behavior: 'smooth' });
        } else {
          submitButton.disabled = false;
          submitButton.textContent = 'Confirmar Presença';
          showToast("Erro: " + data.error, "error");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        submitButton.disabled = false;
        submitButton.textContent = 'Confirmar Presença';
        showToast("Ocorreu um erro ao enviar a confirmação.", "error");
      });
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