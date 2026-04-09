function copyPixKey() {
    const pixKey = "vinicius.mariano.afonso@gmail.com";

    navigator.clipboard.writeText(pixKey)
        .then(() => {
            showToast("Chave Pix copiada!", "success");
        })
        .catch(err => {
            console.error("Erro ao copiar:", err);
            showToast("Não foi possível copiar a chave Pix.", "error");
        });
}