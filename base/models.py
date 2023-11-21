from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    Topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Topic_name
    
class Room(models.Model):
    Host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    Room_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Room"
        db_table = "rooms"

    def __str__(self):
        return self.Room_name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[:50]
