from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.forms import ModelForm

class Like(models.Model):

    like_date = models.DateTimeField(default=timezone.now, verbose_name='date liked')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def serialize(self):
        return {
            "id": self.pk,
        }

class Post(models.Model):

    post_content = models.TextField(max_length=512, blank=False)
    post_likes = models.ManyToManyField(Like, blank=True, related_name='Post')
    post_date = models.DateTimeField(default=timezone.now, verbose_name='date posted')


    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.post_content

    def serialize(self):
        return {
            "id": self.pk,
            "post_content": self.post_content,
            "post_date": self.post_date
        }

class User(AbstractUser):
    
    posts_owner = models.ManyToManyField(Post, blank=True, related_name='owner')
    likes_owner = models.ManyToManyField(Like, blank=True, related_name='owner')

    def serialize(self):
        return {
            "id": self.pk,
            "name": self.username,
            "posts_owner": [post.post_content for post in self.posts_owner.all()]
        }

    def __str__(self):
        return self.username

class Following(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')