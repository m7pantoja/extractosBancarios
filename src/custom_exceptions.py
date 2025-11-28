class FileProcessingError(Exception):
    """Error al procesar archivos."""
    pass

class SchemaValidationError(Exception):
    """Error al validar esquema."""
    pass

class DateConversionError(Exception):
    """Error al convertir fecha."""
    pass

class ModelDownloadError(Exception):
    """Error al descargar el modelo."""
    pass
