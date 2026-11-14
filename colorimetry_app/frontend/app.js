
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const placeholder = document.getElementById("placeholder");
const imageWrapper = document.getElementById("imageWrapper");
const markers = document.getElementById("markers");
const selectionStatus = document.getElementById("selectionStatus");

let selectedPart = null;

const selections = {
    skin: null,
    eyes: null,
    hair: null
};

// Cargar fotografía
imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];

    if (!file) return;

    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;
    imagePreview.style.display = "block";
    placeholder.style.display = "none";

    selections.skin = null;
    selections.eyes = null;
    selections.hair = null;

    markers.innerHTML = "";
    selectedPart = null;
    selectionStatus.textContent = "Elegí qué punto querés seleccionar.";
});

// Elegir qué característica seleccionar
document.querySelectorAll("[data-part]").forEach(button => {
    button.addEventListener("click", function () {
        selectedPart = this.dataset.part;

        selectionStatus.textContent =
            `Ahora hacé clic sobre la zona de ${selectedPart}.`;
    });
});

// Seleccionar punto sobre la fotografía
imagePreview.addEventListener("click", function (event) {
    if (!selectedPart) {
        selectionStatus.textContent =
            "Primero elegí piel, ojos o cabello.";
        return;
    }

    const rect = imagePreview.getBoundingClientRect();

    const x = Math.round(
        (event.clientX - rect.left) *
        imagePreview.naturalWidth / rect.width
    );

    const y = Math.round(
        (event.clientY - rect.top) *
        imagePreview.naturalHeight / rect.height
    );

    selections[selectedPart] = { x, y };

    // Crear marcador visual
    const marker = document.createElement("div");
    marker.className = "marker";
    marker.style.left = `${(x / imagePreview.naturalWidth) * 100}%`;
    marker.style.top = `${(y / imagePreview.naturalHeight) * 100}%`;

    marker.style.backgroundColor = {
        skin: "#E8A080",
        eyes: "#3985D6",
        hair: "#333333"
    }[selectedPart];

    // Reemplazar marcador anterior de esa característica
    const oldMarker = markers.querySelector(
        `[data-marker="${selectedPart}"]`
    );

    if (oldMarker) oldMarker.remove();

    marker.dataset.marker = selectedPart;
    markers.appendChild(marker);

    selectionStatus.textContent =
        `${selectedPart}: x=${x}, y=${y}`;

    selectedPart = null;
});

// Consultar coordenadas desde la consola
window.getSelections = function () {
    return selections;
};


const analyzeButton = document.getElementById("analyzeButton");
const analysisResult = document.getElementById("analysisResult");

analyzeButton.addEventListener("click", async function () {
    const file = imageInput.files[0];

    // Verificar que haya una fotografía
    if (!file) {
        analysisResult.textContent = "Primero cargá una fotografía.";
        return;
    }

    // Verificar que estén seleccionados los tres puntos
    if (!selections.skin || !selections.eyes || !selections.hair) {
        analysisResult.textContent =
            "Tenés que seleccionar piel, ojos y cabello.";
        return;
    }

    // Preparar los datos para enviar
    const formData = new FormData();

    formData.append("file", file);
    formData.append("selections_json", JSON.stringify(selections));

    analysisResult.textContent = "Analizando fotografía...";
    analyzeButton.disabled = true;

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail?.message || "Error al analizar la fotografía."
            );
        }

        renderAnalysis(result);

        console.log("Resultado del análisis:", result);

    } catch (error) {
        analysisResult.textContent = error.message;
        console.error("Error:", error);

    } finally {
        analyzeButton.disabled = false;
    }
});

function renderAnalysis(result) {
    const analysis = result.analysis;

    console.log("Categoría luminosidad ojos:", analysis.eyes.luminosity_category);
    console.log("Categoría cromaticidad ojos:", analysis.eyes.chromaticity_category);

    const colors = [
        {
            name: "Piel",
            data: analysis.skin
        },
        {
            name: "Ojos",
            data: analysis.eyes
        },
        {
            name: "Cabello",
            data: analysis.hair
        }
    ];

    // Traducción de las categorías del backend
    const luminosityLabels = {
        light: "Clara",
        medium: "Media",
        dark: "Oscura"
    };

    const chromaticityLabels = {
        soft: "Suave",
        medium: "Media",
        intense: "Intensa"
    };

    analysisResult.innerHTML = `
        <h2 class="results-title">Tu análisis de color</h2>

        <h3>Paleta recomendada: ${result.palette.name}</h3>

        <div class="color-grid">
            ${result.palette.colors.map(color => `
                <div class="color-card">
                    <div
                        class="color-sample"
                        style="background-color: ${color}">
                    </div>
                    <p class="color-hex">${color}</p>
                </div>
            `).join("")}
        </div>
        <h3>Colores identificados</h3>

        <div class="color-grid">
            ${colors.map(color => {
                const { r, g, b } = color.data.rgb;

                const hex = "#" +
                    [r, g, b]
                    .map(value => value.toString(16).padStart(2, "0"))
                    .join("")
                    .toUpperCase();

                const luminosity =
                    luminosityLabels[color.data.luminosity_category];

                const chromaticity =
                    chromaticityLabels[color.data.chromaticity_category];

                console.log(color.name, {
                    luminosity,
                    chromaticity
                });

                return `
                    <div class="color-card">

                        <div
                            class="color-sample"
                            style="background-color: ${hex}">
                        </div>

                        <h3>${color.name}</h3>

                        <p class="color-hex">${hex}</p>

                        <div class="color-characteristics">

                            <p>
                                <strong>Luminosidad:</strong>
                                ${luminosity || "Sin clasificar"}
                            </p>

                            <p>
                                <strong>Cromaticidad:</strong>
                                ${chromaticity || "Sin clasificar"}
                            </p>

                        </div>
                    </div>
                `;
            }).join("")}
        </div>

        <div class="contrast-section">
            <h3>Contraste de luminosidad</h3>

            <p>HSV: ${(analysis.luminosity_contrast.hsv * 100).toFixed(2)}%</p>

            <div class="contrast-bar">
                <div
                    class="contrast-fill"
                    style="width: ${analysis.luminosity_contrast.hsv * 100}%">
                </div>
            </div>

            <p>LAB: ${analysis.luminosity_contrast.lab.toFixed(2)} / 100</p>

            <div class="contrast-bar">
                <div
                    class="contrast-fill"
                    style="width: ${analysis.luminosity_contrast.lab}%">
                </div>
            </div>
        </div>
    `;
}
