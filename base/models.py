from django.db import models

class Room(models.Model):
    Room_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Room"
        db_table = "rooms"

    def __str__(self):
        return self.Room_name
