from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # Importing the signals here ensures they are registered 
        # as soon as the blog app is loaded.
        import blog.signals