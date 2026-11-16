# Análisis de colorimetría personal

Aplicación web para explorar relaciones de color a partir de una fotografía. Permite seleccionar un punto de la piel, los ojos y el cabello; el backend estima el color de cada zona, calcula características en RGB, HSV y CIELAB, y devuelve una estación y una paleta orientativas.

## Alcance y limitaciones

El color se estima usando la mediana de una región de hasta 5 × 5 píxeles alrededor de cada punto seleccionado. La clasificación de estaciones es una aproximación inicial del proyecto, no un diagnóstico ni una evaluación profesional. La iluminación, el balance de blancos, la calidad de la fotografía y la ubicación de los puntos pueden cambiar los resultados.

## Requisitos

- Python 3.9 o posterior.
- pip.

Las dependencias del backend están declaradas en `requirements.txt`.

## Instalación y ejecución en Windows

Abrí PowerShell en la carpeta `colorimetry_app` (la que contiene este README) y ejecutá:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload
```

Luego abrí <http://127.0.0.1:8000/>. La interfaz y la API se sirven desde FastAPI; ejecutarla desde un servidor estático independiente puede hacer que las solicitudes de análisis no encuentren la API.

La documentación interactiva de la API está disponible en <http://127.0.0.1:8000/docs>.

## Uso

1. Cargá una fotografía.
2. Elegí piel, ojos o cabello y hacé clic en el punto correspondiente de la imagen. Repetí para las tres características.
3. Seleccioná **Analizar fotografía** para ver los colores estimados, sus categorías, el contraste global y la paleta recomendada.

Se aceptan imágenes PNG, JPEG, WEBP y BMP de hasta 10 MiB. Las coordenadas seleccionadas corresponden a la imagen original.

## API

- `GET /api/health`: comprueba que el servidor esté activo.
- `POST /api/analyze`: recibe una imagen y un campo `selections_json` con las coordenadas de los tres puntos.

Ejemplo del contenido de `selections_json`:

```json
{
  "skin": { "x": 250, "y": 180 },
  "eyes": { "x": 270, "y": 130 },
  "hair": { "x": 300, "y": 60 }
}
```

La respuesta contiene los datos del análisis y la paleta recomendada. Los errores de validación y procesamiento se devuelven con un código y un mensaje.

## Pruebas

Desde la carpeta `colorimetry_app`, ejecutá en PowerShell:

```powershell
$env:PYTHONPATH = "backend"
python -m unittest discover -s tests -v
```

## Estructura del proyecto

```text
backend/
  app/
    core/       Procesamiento de imágenes y análisis de color
    routers/    Endpoints de la API
    main.py     Configuración de FastAPI y publicación del frontend
frontend/       Interfaz HTML, CSS y JavaScript
tests/          Pruebas automatizadas
archivos extra/ Archivos de datos complementarios
```