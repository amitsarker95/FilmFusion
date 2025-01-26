from django.db import models

# Create your models here.


class Movies(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
