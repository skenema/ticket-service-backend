ticket_schema = {
    "type": "object",
    "properties": {
        "seatNumbers" : {"type": "string"}, 
        "cinema" : {"type": "string"}, 
        "showtime" : {"type": "string"}
    },
    "required": ["seatNumbers", "cinema", "showtime"],
    "additionalProperties": False
}