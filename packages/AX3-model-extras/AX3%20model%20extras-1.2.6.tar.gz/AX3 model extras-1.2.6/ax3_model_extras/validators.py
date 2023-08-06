from django.core.validators import BaseValidator

import magic


class FileSizeValidator(BaseValidator):
    """Validate a file size. Size must be given in KB.
    """
    message = 'El peso del archivo debe ser menor al tamaño máximo permitido'
    code = 'file_size'

    def compare(self, a, b):
        return a.size > 1024 * b


class ImageDimensionValidator(BaseValidator):
    """Validate an image dimensions. Should receive a tuple like (width, height).
    """
    message = 'La imagen debe tener las dimensiones especificadas'
    code = 'file_dimension'

    def compare(self, a, b):
        width, height = b
        if width == 0:
            return a.height != height

        if height == 0:
            return a.width != width

        return a.width != width or a.height != height


class MimetypeValidator(BaseValidator):
    """
    Validate a file mimetype.
    """
    message = 'El documento no tiene el formato correcto'
    code = 'file_mimetype'

    def compare(self, a, b):
        try:
            mime = magic.from_buffer(a.read(), mime=True)
            return mime not in b
        except AttributeError:
            return True
