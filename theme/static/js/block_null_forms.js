document
  .getElementById("rsvp-form")
  .addEventListener("submit", function (event) {
    const checkedBoxes = document.querySelectorAll(
      'input[name="confirmacao"]:checked'
    );

    if (checkedBoxes.length === 0) {
      event.preventDefault();
      alert(
        "Por favor, selecione pelo menos um convidado para confirmar presença."
      );
    }
  });
