TASK_EVENT_LISTENERS_JSON_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["class", "priority"],
        "properties": {
            "class": {"type": "string"},
            "args": {"type": "array"},
            "kwargs": {"type": "object"},
            "priority": {"type": "integer"},
        },
    },
}
