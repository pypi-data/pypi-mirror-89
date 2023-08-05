#!/usr/bin/env python3

from json_schema_himarc.validation import (
    _get_schema,
    get_himarc_validation_errors,
    validate_himarc,
)


def test_get_schema():
    schema = _get_schema()
    assert isinstance(schema, dict)
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["$id"] == "http://issn.org/record.schema.json"
    assert schema["title"] == "MARC 21 Format for Bibliographic Data in ISSN+"
    assert (
        schema["description"]
        == "MARC 21 Format for Bibliographic Data in ISSN+"
    )


def test_validate_himarc(valid_himarc, invalid_himarc, empty_dict):
    assert validate_himarc(valid_himarc) is True
    assert validate_himarc(invalid_himarc) is False
    assert validate_himarc(empty_dict) is False


def test_get_himarc_errors(valid_himarc, invalid_himarc, empty_dict):
    assert list(get_himarc_validation_errors(valid_himarc)) == []

    errors = list(get_himarc_validation_errors(invalid_himarc))
    assert len(errors) == 8
    err_msgs = [f"{err.validator}: {err.message}" for err in errors]

    assert [
        "additionalProperties: Additional properties are not allowed ('x' was unexpected)",  # noqa
        "required: '10' is a required property",
        "required: '11' is a required property",
        "required: '17' is a required property",
        "enum: 'x' is not one of ['a', 'c', 'd', 'f', 'g', 'h', 'k', 'm', 'o', 'q', 'r', 's', 't', 'v', 'z']",  # noqa
        "anyOf: {'positions': {'18': 'a', '19': 'r', '20': '|', '21': 'p', '22': ' ', '23': ' ', '24': ' ', '25': ' ', '26': ' ', '27': ' ', '28': '12987', '29': '0', '30': ' ', '31': ' ', '32': ' ', '33': 'a', '34': '0', '38': ' ', '39': ' ', '00-05': '190816', '06': 'c', '07-10': '1869', '11-14': '9999', '15-17': 'enkore', '35-37': 'eng'}} is not valid under any of the given schemas",  # noqa
        "additionalProperties: Additional properties are not allowed ('x' was unexpected)",  # noqa
        "pattern: 'GBRA' does not match '^([a-zA-Z]{3}|[a-zA-Z]{2}|[0-9]{3})$'",  # noqa
    ] == err_msgs

    errors = list(get_himarc_validation_errors(empty_dict))
    assert len(errors) == 1
    err = errors[0]
    assert err.message == "'fields' is a required property"
