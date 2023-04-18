ticket_schema = {
    "type": "object",
    "properties": {
        "title" : {"type": "string"},
        "seat_number" : {
            "type": "array",
            "items": {"type": "integer"}
        }, 
        "cinema" : {"type": "string"}, 
        "showtime" : {"type": "string", "format": "date-time"}
    },
    "required": ["seat_number", "cinema", "showtime"],
    "additionalProperties": False
}