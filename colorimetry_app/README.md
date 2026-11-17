# Análisis de colorimetría personal

Aplicación web para explorar relaciones de color a partir de una fotografía. Permite seleccionar un punto de la piel, los ojos y el cabello; el backend estima el color de cada zona, calcula características en RGB, HSV y CIELAB, y devuelve una estación y una paleta orientativas.

## Alcance y limitaciones

El color se estima usando la mediana de una región de hasta 5 × 5 píxeles alrededor de cada punto seleccionado. La clasificación de estaciones es una aproximación inicial del proyecto, no un diagnóstico ni una evaluación profesional. La iluminación, el balance de blancos, la calidad de la fotografía y la ubicación de los puntos pueden cambiar los resultados.

## Criterios de color y estimación de estación

Los cortes de luminosidad (`L*`: 60.33 y 64.32) y cromaticidad (`C*`: 20.04 y 22.05) se calcularon sobre 600 mediciones de piel: 150 sujetos del origen 1 (UK), con una medición por sujeto en cada una de estas zonas: mejilla (código 2), pómulo (3), mentón (4) y frente (6). Se agruparon las cuatro zonas y se usaron los percentiles 33,33 y 66,67 con interpolación lineal, redondeados a dos decimales.

Estos umbrales describen únicamente la distribución de las mediciones de piel. Los ojos y el cabello se muestran con sus valores continuos de `L*` y `C*`; no se les asignan categorías usando los cortes de piel. La base de datos no contiene etiquetas de estaciones para validar la heurística.

La heurística toma la piel como referencia para la temperatura (delta = `b* - a*`: cálida si delta > 0, fría si delta < 0 e indeterminada si delta = 0) y para las categorías de luminosidad y cromaticidad. La luminosidad de piel elige la estación base: cálida y clara corresponde a Primavera; cálida y media u oscura, a Otoño; fría y clara, a Verano; fría y media u oscura, a Invierno. Ojos y cabello aportan el contraste: se considera alto cuando el rango de `L*` entre los tres puntos es de al menos 20. La cromaticidad de piel y el contraste ajustan la confianza:

- Confianza alta: cromaticidad y contraste acompañan la estación.
- Confianza media: solo uno de esos indicadores coincide.
- Confianza baja: `|delta| <= 3`, ninguno de esos indicadores coincide, la temperatura es indeterminada o no se asigna estación.

Es una propuesta exploratoria del proyecto, no una regla validada con diagnósticos o etiquetas de estación. Los umbrales de piel tampoco se validaron para clasificar estaciones.

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
3. Seleccioná **Analizar fotografía** para ver los valores continuos de los tres puntos, la clasificación orientativa de piel, el contraste global y la paleta sugerida.

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
archivos extra/
  Skin Database 1-92.xlsx                 Libro original con el diccionario de códigos
  Skin Database 1-92.xlsx - Database.csv Exportación de la hoja de mediciones
```