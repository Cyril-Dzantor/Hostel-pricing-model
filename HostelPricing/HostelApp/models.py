from django.db import models

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    room_size = models.PositiveSmallIntegerField()
    infrastructure = models.JSONField(default=list)
    appliances = models.JSONField(default=list)
    image = models.ImageField(upload_to='hostel_images/', null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.location}"
