"""
Conversion between bytes and images in memory.

`ImageCodec` is used by the service to:
  - inspect an uploaded file (is it an image? which format and size?),
  - open a stored file as an image ready to be processed,
  - encode the result of an operation back to bytes, in memory, before the
    storage writes it to disk.

¿Por qué conviene trabajar así en bytes?
Tiene varias ventajas:
- Memoria: podemos procesar la imagen sin tener que guardarla primero en el disco.
- Flexibilidad: podemos abrirla, verificarla, modificarla o convertirla directamente desde memoria.
- Integración: Pillow permite trabajar directamente con bytes mediante BytesIO.
- Almacenamiento: si necesitamos guardar el archivo, podemos hacerlo después de validarlo.

Trabajamos con bytes porque permiten recibir y procesar imágenes directamente en memoria, evitando depender del almacenamiento físico durante las primeras etapas del procesamiento.
encaja muy bien con FastAPI
"""

from dataclasses import dataclass #permite crear clases destinadas principalmente a almacenar datos.
from io import BytesIO #permite trabajar con bytes como si fueran un archivo en memoria. permite que Pillow trate esos bytes como un archivo.

from PIL import Image

from app.core.exceptions import InvalidFile


@dataclass(frozen=True) #significa que, una vez creado el objeto, sus atributos no se pueden modificar.
class ImageInfo:
    format: str  # as in Pillow's `Image.format` ("PNG", "JPEG", "GIF", ...)
    width: int
    height: int


class ImageCodec:
    def inspect(self, content: bytes) -> ImageInfo:
        """Opens `content` and returns its format (detected by content) and size.

        Raises `InvalidFile` if it cannot be opened as an image (includes empty
        content). It does NOT check the allowed formats: that is done by the service.
        """
        try:
            with Image.open(BytesIO(content)) as image:
                image.verify() #Este método comprueba que el archivo tenga una estructura válida de imagen.
                #Si la imagen supera la verificación, el método termina normalmente y devuelve None.
                #Si detecta que el archivo está dañado o tiene una estructura inválida, lanza una excepción (un error).

                return ImageInfo(format=image.format, width=image.width, height=image.height)
        except Exception as exc:
            raise InvalidFile() from exc

    def open(self, content: bytes) -> Image.Image: #Esta función también recibe bytes, pero su objetivo es distinto: abrir la imagen para trabajar con sus píxeles.
        """Opens the bytes of a stored file as an image ready to be processed.

        The color mode is normalized to L, RGB or RGBA, so the operations only
        have to deal with those three.
        """
        image = Image.open(BytesIO(content))
        image.load() #decodifica y carga los píxeles de la imagen en memoria.
        if image.mode in ("L", "RGB", "RGBA"):
            return image
        if image.mode == "1":
            return image.convert("L")
        if image.mode in ("LA", "PA") or (image.mode == "P" and "transparency" in image.info):
            return image.convert("RGBA")
        return image.convert("RGB")

#    inspect(): recibe la imagen en bytes, intenta abrirla para verificar que sea una imagen válida y devuelve información sobre ella: formato, ancho y alto. No prepara la imagen para procesarla.
#open(): también recibe los bytes, pero esta vez carga la imagen y la prepara para trabajar con sus píxeles. Para eso normaliza su modo de color a L, RGB o RGBA.

