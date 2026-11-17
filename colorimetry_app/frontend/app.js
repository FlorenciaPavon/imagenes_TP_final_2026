
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const placeholder = document.getElementById("placeholder");
const imageWrapper = document.getElementById("imageWrapper");
const markers = document.getElementById("markers");
const selectionStatus = document.getElementById("selectionStatus");
const analyzeButton = document.getElementById("analyzeButton");
const analysisResult = document.getElementById("analysisResult");
const partButtons = [...document.querySelectorAll("[data-part]")];

const partLabels = {
    skin: "Piel",
    eyes: "Ojos",
    hair: "Cabello"
};

const markerColors = {
    skin: "#D99777",
    eyes: "#5485A6",
    hair: "#4A403A"
};

let selectedPart = null;
let previewURL = null;

const selections = {
    skin: null,
    eyes: null,
    hair: null
};

imagePreview.addEventListener("load", function () {
    imageWrapper.hidden = false;
    placeholder.hidden = true;
    partButtons.forEach(button => {
        button.disabled = false;
    });
    selectionStatus.textContent = "Elegí piel, ojos y cabello para marcar sus puntos.";
});

imagePreview.addEventListener("error", function () {
    if (!previewURL) return;

    URL.revokeObjectURL(previewURL);
    previewURL = null;
    imageInput.value = "";
    imageWrapper.hidden = true;
    placeholder.hidden = false;
    placeholder.textContent = "No se pudo cargar esa imagen. Probá con otro archivo.";
    partButtons.forEach(button => {
        button.disabled = true;
    });
    selectionStatus.textContent = "No se pudo cargar la fotografía.";
    updateAnalyzeButton();
});

function updateAnalyzeButton() {
    analyzeButton.disabled = !imageInput.files[0] ||
        !selections.skin ||
        !selections.eyes ||
        !selections.hair;
}

// Cargar fotografía
imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];

    if (!file) return;

    if (previewURL) URL.revokeObjectURL(previewURL);
    previewURL = URL.createObjectURL(file);

    imagePreview.src = previewURL;
    imageWrapper.hidden = true;
    placeholder.hidden = false;
    placeholder.textContent = "Cargando fotografía...";

    selections.skin = null;
    selections.eyes = null;
    selections.hair = null;

    markers.innerHTML = "";
    selectedPart = null;
    partButtons.forEach(button => {
        button.disabled = true;
        button.setAttribute("aria-pressed", "false");
    });
    analysisResult.hidden = true;
    analysisResult.textContent = "";
    updateAnalyzeButton();
    selectionStatus.textContent = "Cargando la fotografía...";
});

// Elegir qué característica seleccionar
partButtons.forEach(button => {
    button.addEventListener("click", function () {
        selectedPart = this.dataset.part;

        partButtons.forEach(partButton => {
            partButton.setAttribute(
                "aria-pressed",
                String(partButton === this)
            );
        });

        selectionStatus.textContent =
            `Ahora hacé clic sobre la zona de ${partLabels[selectedPart].toLowerCase()}.`;
    });
});

// Seleccionar punto sobre la fotografía
imageWrapper.addEventListener("click", function (event) {
    if (!selectedPart) {
        selectionStatus.textContent =
            "Primero elegí piel, ojos o cabello.";
        return;
    }

    const rect = imagePreview.getBoundingClientRect();

    const x = Math.max(0, Math.min(imagePreview.naturalWidth - 1, Math.floor(
        (event.clientX - rect.left) *
        imagePreview.naturalWidth / rect.width
    )));

    const y = Math.max(0, Math.min(imagePreview.naturalHeight - 1, Math.floor(
        (event.clientY - rect.top) *
        imagePreview.naturalHeight / rect.height
    )));

    selections[selectedPart] = { x, y };

    const marker = document.createElement("div");
    marker.className = "marker";
    marker.style.left = `${(x / imagePreview.naturalWidth) * 100}%`;
    marker.style.top = `${(y / imagePreview.naturalHeight) * 100}%`;
    marker.style.backgroundColor = markerColors[selectedPart];
    marker.dataset.label = partLabels[selectedPart];
    marker.setAttribute("aria-label", partLabels[selectedPart]);

    const oldMarker = markers.querySelector(
        `[data-marker="${selectedPart}"]`
    );

    if (oldMarker) oldMarker.remove();

    marker.dataset.marker = selectedPart;
    markers.appendChild(marker);

    selectionStatus.textContent =
        `${partLabels[selectedPart]}: punto marcado (x=${x}, y=${y}).`;

    selectedPart = null;
    partButtons.forEach(button => button.setAttribute("aria-pressed", "false"));
    updateAnalyzeButton();
});

// Consultar coordenadas desde la consola
window.getSelections = function () {
    return selections;
};


analyzeButton.addEventListener("click", async function () {
    const file = imageInput.files[0];

    if (!file) {
        analysisResult.hidden = false;
        analysisResult.textContent = "Primero cargá una fotografía.";
        return;
    }

    if (!selections.skin || !selections.eyes || !selections.hair) {
        analysisResult.hidden = false;
        analysisResult.textContent =
            "Tenés que seleccionar piel, ojos y cabello.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("selections_json", JSON.stringify(selections));

    analysisResult.hidden = false;
    analysisResult.textContent = "Analizando fotografía...";
    analyzeButton.disabled = true;

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            body: formData
        });

        let result;
        try {
            result = await response.json();
        } catch {
            throw new Error("El servidor devolvió una respuesta que no se pudo leer.");
        }

        if (!response.ok) {
            throw new Error(
                result.detail?.message || "Error al analizar la fotografía."
            );
        }

        renderAnalysis(result);
    } catch (error) {
        analysisResult.textContent =
            error instanceof Error
                ? error.message
                : "No se pudo analizar la fotografía.";

    } finally {
        updateAnalyzeButton();
    }
});

function renderAnalysis(result) {
    const analysis = result.analysis;
    const seasonal = result.seasonal_analysis;

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
    const lightnessLabels = {
        light: "Clara",
        medium: "Media",
        dark: "Oscura"
    };

    const chromaLabels = {
        soft: "Suave",
        medium: "Media",
        intense: "Intensa"
    };

    const temperatureLabels = {
        warm: "Cálida",
        cool: "Fría",
        undetermined: "Indeterminada"
    };

    const consistencyLabels = {
        low: "Baja",
        medium: "Media",
        high: "Alta"
    };

    const paletteHeading = seasonal.season === "No determinada"
        ? "Colores seleccionados (sin estación determinada)"
        : `Paleta orientativa: ${result.palette.name}`;

    analysisResult.innerHTML = `
        <h2 id="analysisResultTitle" class="results-title">Tu análisis de color</h2>
        <div class="analysis-note">
            <p>
                La piel guía la estación. Los valores de ojos y cabello se muestran de forma
                continua y aportan contexto de contraste. Los cortes y la estación son
                exploratorios; la luz y la selección de los puntos pueden influir.
            </p>
            <p>
                <strong>Indicador térmico de piel (heurístico):</strong>
                ${temperatureLabels[seasonal.temperature] || "Sin clasificar"}
                &nbsp;·&nbsp;
                <strong>Claridad de piel (L*):</strong>
                ${lightnessLabels[seasonal.lightness] || "Sin clasificar"}
                &nbsp;·&nbsp;
                <strong>Croma de piel (C*):</strong>
                ${chromaLabels[seasonal.chroma] || "Sin clasificar"}
            </p>
            <p>
                <strong>Estación estimada (heurística):</strong> ${seasonal.season}
                &nbsp;·&nbsp;
                <strong>Consistencia de las reglas:</strong>
                ${consistencyLabels[seasonal.rule_consistency] || "Sin clasificar"}
            </p>
        </div>

        <h3 class="result-section-heading">${paletteHeading}</h3>

        <div class="palette-grid">
            ${result.palette.colors.map(color => `
                <div class="color-card palette-card">
                    <div
                        class="color-sample"
                        style="background-color: ${color}">
                    </div>
                    <p class="color-hex">${color}</p>
                </div>
            `).join("")}
        </div>
        <h3 class="result-section-heading">Colores identificados</h3>

        <div class="color-grid">
            ${colors.map(color => {
                const { r, g, b } = color.data.rgb;

                const hex = "#" +
                    [r, g, b]
                    .map(value => value.toString(16).padStart(2, "0"))
                    .join("")
                    .toUpperCase();

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
                                <strong>L*:</strong>
                                ${color.data.lab.l.toFixed(2)}
                            </p>

                            <p>
                                <strong>C*:</strong>
                                ${color.data.chroma.toFixed(2)}
                            </p>

                        </div>
                    </div>
                `;
            }).join("")}
        </div>

        <div class="contrast-section">
            <h3>Rangos entre los puntos seleccionados</h3>

            <p>Rango de V (HSV): ${(analysis.color_ranges.value * 100).toFixed(2)}%</p>

            <div class="contrast-bar">
                <div
                    class="contrast-fill"
                    style="width: ${analysis.color_ranges.value * 100}%">
                </div>
            </div>

            <p>Rango de L* (CIELAB): ${analysis.color_ranges.lightness.toFixed(2)} / 100</p>

            <div class="contrast-bar">
                <div
                    class="contrast-fill"
                    style="width: ${analysis.color_ranges.lightness}%">
                </div>
            </div>
        </div>
    `;
}
