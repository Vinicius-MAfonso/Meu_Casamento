function copyPixKey() {
  const pixKey = "vinicius.mariano.afonso@gmail.com";

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard
      .writeText(pixKey)
      .then(() => {
        showToast("Chave Pix copiada com sucesso!", "success");
      })
      .catch((err) => {
        console.error("Erro ao copiar:", err);
        showToast("Não foi possível copiar a chave Pix.", "error");
      });
  } else {
    // Fallback for older browsers
    const textarea = document.createElement("textarea");
    textarea.value = pixKey;
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      showToast("Chave Pix copiada com sucesso!", "success");
    } catch (err) {
      showToast("Não foi possível copiar a chave Pix.", "error");
    }
    document.body.removeChild(textarea);
  }
}

function initPixBtn() {
  const btnPix = document.getElementById("btn-copy-pix");
  if (btnPix) {
    btnPix.addEventListener("click", copyPixKey);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initPixBtn);
} else {
  initPixBtn();
}