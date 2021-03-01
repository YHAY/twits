join_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "country": {"type": "number"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "country", "device_number"]
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

matching_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "device_number"]
}

choice_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pw": {"type": "string"},
        "device_number": {"type": "string"}
    },
    "required": ["id", "pw", "device_number"]
}
# join_schema = {
#     "type" : "object",
#     "properties" : {
#         "id" : {"type" : "string"},
#         "pw" : {"type" : "string"},
#         "country" : {"type" : "number"},
#         "device_number" : {"type" : "string"}
#     }
# }
#
#
# schema = {
# ...     "type" : "object",
# ...     "properties" : {
# ...         "price" : {"type" : "number"},
# ...         "name" : {"type" : "string"},
# ...     },
# ... }