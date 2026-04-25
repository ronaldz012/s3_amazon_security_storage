class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)

class ConflictException(AppException):
    def __init__(self, message: str = "Conflicto con el estado actual"):
        super().__init__(message, status_code=409)

class InternalException(AppException):
    def __init__(self, message: str = "Error interno del servidor"):
        super().__init__(message, status_code=500)