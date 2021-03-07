join_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "name": {"type": "string"},
        "country": {"type": "number"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "name", "country", "device_number"]
}

del_user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "country": {"type": "number"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "country", "device_number"]
}

login_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "device_number"]
}

# matching_schema = {
#     "type": "object",
#     "properties": {
#         "token": {"type": "string"},
#         "game_auth": {"type": "string"},
#         "rival": {"type": "string"}
#     },
#     "required": ["id", "pw", "device_number"]
# }

choice_schema = {
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "datetime": {"type": "datetime"}
    },
    "required": ["user", "datetime"]
}

result_schema = {
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "datetime": {"type": "datetime"}
    },
    "required": ["user", "datetime"]
}