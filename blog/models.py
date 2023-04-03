from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_link = models.CharField(max_length=150)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
    
# Create Crop yield model
class Crop(models.Model): 
    Year = models.IntegerField(null=False, blank=False)
    Latitude = models.FloatField(null=False, blank=False)
    Longitude = models.FloatField(null=False, blank=False)
    Crop = models.IntegerField(null=False, blank=False)
    Acres = models.IntegerField(null=False, blank=False)
    Measured = models.IntegerField(null=False, blank=False)

# Create weather model
class Weather(models.Model): 
    Year = models.IntegerField(null=False, blank=False)
    Latitude = models.FloatField(null=False, blank=False)
    Longitude = models.FloatField(null=False, blank=False)
    tavg = models.FloatField(null=False, blank=False)
    tmin = models.FloatField(null=False, blank=False)
    tmax = models.FloatField(null=False, blank=False)