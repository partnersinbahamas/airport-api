SCHEMA_JSON_RESPONSE_401 = {
    "description": "Unauthorized",
    "content": {
        "application/json": {
            "schema": {"type": "object"},
            "examples": {
                "Unauthorized": {
                    "value": {"detail": "Authentication credentials were not provided."}
                }
            },
        }
    },
}


SCHEMA_JSON_RESPONSE_403 = {
    "description": "Forbidden",
    "content": {
        "application/json": {
            "schema": {"type": "object"},
            "examples": {
                "Forbidden": {
                    "value": {"detail": "You do not have permission to perform this action."}
                }
            },
        }
    },
}

SCHEMA_JSON_RESPONSE_429 = {
    "description": "Request was throttled",
    "content": {
        "application/json": {
            "schema": {"type": "object"},
            "examples": {
                "RequestThrottled": {
                    "value": {
                        "detail": (
                            "Request was throttled. "
                            "Expected available in {seconds} seconds."
                        )
                    }
                }
            },
        }
    },
}


def schema_default_responses(result, generator, request, public):
    """
    Adding global 401 and 403 response status codes to all service endpoints.
    """
    for path, path_item in result["paths"].items():
        for method, operation in path_item.items():
            if method not in ["get", "post", "put", "patch", "delete"]:
                continue

            responses = operation.get("responses", {})
            responses.setdefault("401", SCHEMA_JSON_RESPONSE_401)
            responses.setdefault("403", SCHEMA_JSON_RESPONSE_403)

            operation["responses"] = responses

    return result
