USER_CREATE = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string",
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        }
    },
    "required": ["username", "password"]
}

AD_CREATE = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "description": {
            "type": "string",
        }
    },
    "required": ["title", "description"]
}