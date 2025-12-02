function copyPixKey() {
    const pixKey = "vinicius.mariano.afonso@gmail.com";

    navigator.clipboard.writeText(pixKey)
        .then(() => {
            alert("Chave Pix copiada!");
        })
        .catch(err => {
            console.error("Erro ao copiar:", err);
            alert("Não foi possível copiar a chave Pix.");
        });
}