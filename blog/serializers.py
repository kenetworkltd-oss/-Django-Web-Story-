from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # This converts our database fields into JSON keys
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body', 'date_published']
        