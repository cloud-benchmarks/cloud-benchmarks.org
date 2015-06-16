import jsonschema

submission_schema = {
    "definitions": {
        "result": {
            "type": "object",
            "properties": {
                "units": {
                    "type": "string",
                },
                "direction": {
                    "type": "string",
                    "default": "asc",
                },
                "value": {
                    "type": "string",
                },
            },
            "required": [
                "value",
            ],
        },
    },
    "type": "object",
    "properties": {
        "version": {
            "type": "string",
            "enum": [
                "1.0",
            ],
        },
        "action": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                },
                "started": {
                    "type": "string",
                },
                "completed": {
                    "type": "string",
                },
                "enqueued": {
                    "type": "string",
                },
                "action": {
                    "type": "object",
                    "properties": {
                        "tag": {
                            "type": "string",
                        },
                        "name": {
                            "type": "string",
                        },
                        "receiver": {
                            "type": "string",
                        },
                        "parameters": {
                            "type": "object",
                        },
                    },
                    "required": [
                        "tag",
                        "name",
                        "receiver",
                        "parameters",
                    ],
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "meta": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "string",
                                },
                                "stop": {
                                    "type": "string",
                                },
                                "composite": {
                                    "$ref": "#/definitions/result"
                                },
                            },
                            "required": [
                                "start",
                                "stop",
                                "composite",
                            ],
                        },
                        "results": {
                            "type": "object",
                            "patternProperties": {
                                "^.*$": {
                                    "$ref": "#/definitions/result"
                                },
                            },
                        },
                    },
                    "required": [
                        "meta",
                        "results",
                    ],
                },
            },
            "required": [
                "status",
                "started",
                "completed",
                "enqueued",
                "action",
                "output",
            ],
        },
        "bundle": {
            "type": "object",
            "properties": {
                "services": {
                    "type": "object",
                    "patternProperties": {
                        "^.*$": {
                            "type": "object",
                            "properties": {
                                "charm": {
                                    "type": "string",
                                },
                                "num_units": {
                                    "type": "integer",
                                },
                                "constraints": {
                                    "type": "object",
                                },
                            },
                            "required": [
                                "charm",
                            ],
                        },
                    },
                },
                "relations": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            },
            "required": [
                "services",
                "relations",
            ],
        },
        "environment": {
            "type": "object",
            "properties": {
                "uuid": {
                    "type": "string",
                },
                "cloud": {
                    "type": "string",
                },
                "provider_type": {
                    "type": "string",
                },
                "region": {
                    "type": "string",
                },
            },
            "required": [
                "uuid",
                "cloud",
                "provider_type",
                "region",
            ],
        },
    },
    "required": [
        "version",
        "action",
        "bundle",
        "environment",
    ],
}


def validate_submission(data):
    """Returns None if ``data`` is a valid submission. Otherwise returns a
    list of validation error messages.

    """
    v = jsonschema.Draft4Validator(submission_schema)
    return list(v.iter_errors(data)) or None
