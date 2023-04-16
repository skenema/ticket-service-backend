ticket_schema = {
    "type": "object",
    "properties": {
        "title" : {"type": "string"},
        "seat_number" : {"type": "integer"}, 
        "cinema" : {"type": "string"}, 
        "showtime" : {"type": "string"}
    },
    "required": ["seat_number", "cinema", "showtime"],
    "additionalProperties": False
}