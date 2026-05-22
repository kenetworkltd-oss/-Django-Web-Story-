from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def log_new_post(sender, instance, created, **kwargs):
    if created:
        # This code only runs when a NEW record is inserted
        print(f"Standard Log: New content created - '{instance.title}'")
        # In a Data Science context, you might trigger a text-analysis 
        # script here to categorize the post automatically.
    else:
        # This runs when an EXISTING record is updated
        print(f"Standard Log: Post '{instance.title}' was updated.")