from django.db import models


class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()
    website = models.URLField(max_length=100)

    def __str__(self):
        return f'Streaming on {self.name}'

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    storyLine = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
