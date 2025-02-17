class GraceError(Exception):
    """Base exception for Grace.

    It could be used to handle any exceptions that are raised by Grace.
    """
    pass


class ConfigError(GraceError):
    """Exception raised for configuration errors.

    This exception is generally raised when the configuration are improperly set up.
    """
    pass


class GeneratorError(GraceError):
    """Exception raised for generator errors."""
    pass


class NoTemplateError(GeneratorError):
    """Exception raised when no template is found for a generator."""
    pass


class ValidationError(GeneratorError):
    """Exception raised for validation errors inside a generator."""
    pass
