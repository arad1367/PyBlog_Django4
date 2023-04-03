from django.contrib import admin
from .models import Post, Crop, Weather

# Register your models here.
admin.site.register(Post)
admin.site.register(Crop)
admin.site.register(Weather)