from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    
    # Adding the photo field
    photo = models.ImageField(upload_to='blog_photos/', null=True, blank=True)
    
    # Adding the category field
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=100)  # Store the username as a CharField
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.username}"
