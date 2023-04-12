from django.db import models

class Tickets(models.Model):
    """Ticket Detail"""
    
    seatNumber = models.CharField(max_length=10)
    cinema = models.CharField(max_length=255)
    showtime = models.DateTimeField()