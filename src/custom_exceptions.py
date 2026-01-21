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

class IAAgentError(Exception):
    """Error al usar el Agente de IA."""
    pass

class CleaningFileError(Exception):
    """Error limpiando archivo."""
    pass

class FileStructureError(Exception):
    """Los archivos no tienen la misma estructura."""
    pass

class InvalidFileError(Exception):
    """El archivo no es válido."""
    pass

class quotaExceededError(Exception):
    """Se ha excedido el límite de uso en todos los modelos de IA disponibles. Por favor intentalo de nuevo más tarde."""
    pass