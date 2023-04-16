from django.db import models

class Tickets(models.Model):
    """Ticket Detail"""
    
    title = models.CharField(max_length=255, default='')
    seat_number = models.IntegerField(default=0)
    cinema = models.CharField(max_length=255)
    showtime = models.DateTimeField()