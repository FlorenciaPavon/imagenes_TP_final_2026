
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

        analysisResult.textContent = JSON.stringify(result, null, 2);

        console.log("Resultado del análisis:", result);

    } catch (error) {
        analysisResult.textContent = error.message;
        console.error("Error:", error);

    } finally {
        analyzeButton.disabled = false;
    }
});
