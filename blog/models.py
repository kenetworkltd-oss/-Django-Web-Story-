from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Performance optimized title
    title = models.CharField(max_length=200, db_index=True)
    
    # Use 'content' to match your PostForm
    content = models.TextField() 
    
    # Use 'status' to match your PostForm
    status = models.CharField(max_length=10, default='draft')
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    
    date_published = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # Keeping your high-performance indexes
        indexes = [
            models.Index(fields=['title', 'date_published']),
        ]

    def __str__(self):
        return self.title