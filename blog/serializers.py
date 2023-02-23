from rest_framework import serializers # turn object data to json
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'author_link', 'title', 'content', 'date_posted']