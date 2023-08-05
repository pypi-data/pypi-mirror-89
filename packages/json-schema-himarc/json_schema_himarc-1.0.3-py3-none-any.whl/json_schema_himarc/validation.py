#!/usr/bin/env python3

"""Validate instance using Himarc JSON schema"""

import json
import os
from collections.abc import Iterable
from typing import Any, Dict

from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

__all__ = ["validate_himarc", "get_himarc_validation_errors"]


SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema")
SCHEMA_FILENAME = "himarc.schema.json"


def _get_schema() -> Dict[str, Any]:
    """Get Himarc JSON schema data."""
    path = os.path.join(SCHEMA_DIR, SCHEMA_FILENAME)
    with open(path, "r") as json_schema_file:
        return json.load(json_schema_file)


def validate_himarc(instance: Dict[str, Any]) -> bool:
    """Validate himarc instance using JSON schema validator."""
    try:
        schema = _get_schema()
        validator = Draft7Validator(schema)
        validator.validate(instance)
        return True
    except ValidationError:
        return False


def get_himarc_validation_errors(
    instance: Dict[str, Any]
) -> Iterable[ValidationError]:
    """Get himarc instance errors using JSON schema validator.

    Returns an iterable of
    <https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError>
    """
    schema = _get_schema()
    validator = Draft7Validator(schema)
    return validator.iter_errors(instance)
