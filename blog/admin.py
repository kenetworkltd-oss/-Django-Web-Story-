from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # These names MUST match the names in models.py exactly
    list_display = ('title', 'author', 'date_published')
    search_fields = ('title', 'body')
    list_filter = ('date_published', 'author')