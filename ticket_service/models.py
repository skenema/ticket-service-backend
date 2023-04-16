from django.db import models

class Tickets(models.Model):
    """Ticket Detail"""

    # 0 is a placeholder variable. I put this to prevent it from being null.
    seat_id = models.IntegerField(default=0) # must not be null
    showtime_id = models.IntegerField(default=0) # must not be null
    cinema = models.CharField(max_length=255)
    start_time = models.DateTimeField()