class GraceError(Exception):
    pass


class ConfigError(GraceError):
    pass


class GeneratorError(GraceError):
    pass


class ValidationError(GeneratorError):
    pass
