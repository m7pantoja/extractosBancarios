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
    """Error al descargar el modelo de GCS."""
    pass

class HashGenerationError(Exception):
    """Error al generar hash."""
    pass

class DataUploadError(Exception):
    """Error al subir datos a BigQuery."""
    pass
