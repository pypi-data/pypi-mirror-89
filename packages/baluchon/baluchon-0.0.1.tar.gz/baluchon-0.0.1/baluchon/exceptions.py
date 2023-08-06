# Manager
class NoChangeException(Exception):
    pass


class NoMigrationException(Exception):
    pass


class InvalidVersionException(Exception):
    pass


class LockedDatabaseException(Exception):
    pass


class LockTimeoutException(Exception):
    pass


class ShortLimitException(Exception):
    def __init__(self, version):
        self.error_code = "short_limit"
        self.msg = f"Limit {version} was too short."


class DirtyVersionException(Exception):
    def __init__(self, version):
        self.error_code = "dirty_version"
        self.msg = f"Dirty database version {version}. Fix and force version."


# Database
class ConnectionNoSetException(Exception):
    pass


# Validator
class ValidationError(Exception):
    pass


class MissingValidationError(Exception):
    pass


# Source
class InvalidMigrationSource(Exception):
    pass


class SourceAlreadyOpenedException(Exception):
    pass

