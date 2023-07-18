from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=256, blank=False)
    text  = models.TextField(blank=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date =  models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_app_name:draft-blogs')

    def publish_blog(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_approve_comments(self):
        return self.blog_comments.filter(approve_commet = True)

class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name='blog_comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True)
    approve_commet = models.BooleanField(default=False)

    def approve_comments(self):
        self.approve_commet = True
        self.save()        

    def __str__(self) -> str:
        return self.text
