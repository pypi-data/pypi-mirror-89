import json
from cerberus import Validator


class ValidationException(Exception):
    def __init__(self, errors):
        super().__init__(json.dumps(errors))


class RaisingValidator(Validator):
    """
    Subclass of cerberus.Validator that will raise if the validation fails.
    """

    def validate(self, *args, **kwargs):
        r = super().validate(*args, **kwargs)
        if r:
            return r
        raise ValidationException(self.errors)
