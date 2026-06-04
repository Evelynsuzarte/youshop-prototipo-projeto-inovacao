async function generate() {
    const get = id => document.getElementById(id);

    const fields = {
        product_key: get("product_key").value,
        product_price: get("product_price").value.trim(),
        creator_name: get("creator_name").value.trim(),
        creator_audience: get("creator_audience").value.trim(),
        creator_network: get("creator_network").value,
        creator_tone: get("creator_tone").value
    };

    if (!fields.product_price || !fields.creator_name || !fields.creator_audience)
        return mostrarErro("Preencha seu nome, público-alvo e preço.");

    get("btn").disabled = true;
    get("loading").style.display = "block";
    get("results").style.display = "none";
    get("error").style.display = "none";

    try {
        const res = await fetch("/generate", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(fields)
        });

        const {success, data, error} = await res.json();

        if (!success) throw new Error(error);

        get("res-angle").textContent = data.angulo_unico;
        get("res-justificativa").textContent = data.justificativa;

        ["video", "legenda", "email"].forEach(tipo => {
            get(`res-${tipo}`).innerHTML =
                `<button class="copy-btn" onclick="copiarTexto('res-${tipo}')">Copiar</button>` +
                data[tipo === "video" ? "roteiro_video" : tipo];
        });

        get("results").style.display = "block";

    } catch (e) {
        mostrarErro(e.message);
    } finally {
        get("btn").disabled = false;
        get("loading").style.display = "none";
    }
}

function mostrarErro(msg) {
    error.textContent = "⚠️ " + msg;
    error.style.display = "block";
}

function mudarabas(tab, btn) {
    document.querySelectorAll(".tab,.tab-content")
        .forEach(e => e.classList.remove("active"));

    btn.classList.add("active");
    document.getElementById(`tab-${tab}`).classList.add("active");
}

function copiarTexto(id) {
    const box = document.getElementById(id);
    const btn = box.querySelector(".copy-btn");

    navigator.clipboard.writeText(
        box.innerText.replace("Copiar", "").trim()
    );

    btn.textContent = "Copiado!";
    setTimeout(() => btn.textContent = "Copiar", 2000);
}