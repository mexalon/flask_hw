import jsonschema
from flask import request


def validate(source: str, req_schema: dict):
    """Валидатор входящих запросов"""

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                jsonschema.validate(
                    instance=getattr(request, source), schema=req_schema,
                )
            except jsonschema.ValidationError:
                raise Exception('Data err')

            result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator
