from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # We specify exactly which fields the user is allowed to edit.
        # This prevents "Mass Assignment" vulnerabilities.
        fields = ['title', 'content', 'status']
        
        # We can add 'widgets' to give the HTML specific styles or classes
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        
