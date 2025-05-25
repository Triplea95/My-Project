from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.conf import settings



class User(AbstractUser):
    # Additional custom fields
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_reporter = models.BooleanField(default= False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to= 'profiles/', blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    id= models.AutoField(primary_key= True)
    name= models.CharField(max_length=100 , unique= True)
    slug = AutoSlugField(populate_from = ['name'], unique= True, blank= True)
    description = models.TextField(max_length= 250, blank= True)

    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from = ['name'])

    def __str__(self):
        return self.name

    
class NewsItem(models.Model):
    id = models.AutoField(primary_key= True)
    title = models.CharField(max_length= 100)
    slug = AutoSlugField(populate_from = ['title'], unique= True, blank= True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class NewsImage(models.Model):
    news_item= models.ForeignKey(NewsItem,  on_delete=models.SET_NULL, related_name= 'images')
    news_item = models.ForeignKey('NewsItem', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.news_item.title}"
    


class Comment(models.Model):
    news_item = models.ForeignKey('NewsItem', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_approved = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.news_item.title}"



class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    news_item = models.ForeignKey('NewsItem', on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news_item')  # Prevents duplicate bookmarks
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked '{self.news_item.title}'"