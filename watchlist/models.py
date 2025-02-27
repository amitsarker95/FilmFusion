from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()
    website = models.URLField(max_length=100)

    def __str__(self):
        return f'Streaming on {self.name}'

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    storyLine = models.TextField()
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ['title', 'platform']
        ordering = ['-avg_rating']
    


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField()
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID: {self.id} Rate : {self.rating} | Show name : {self.watchlist.title} | Username : {self.review_user.username}'
    
    class Meta:
        unique_together = ['watchlist', 'review_user']
        ordering = ['-created']


# class User(models.Model):
#     pass