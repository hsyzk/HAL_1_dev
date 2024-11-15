from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import uuid
import os
from django.core.validators import FileExtensionValidator


class Account(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    account_image = models.ImageField(upload_to="profile_pics",blank=True,validators=[FileExtensionValidator(['jpg', 'png'])])
    
    def __str__(self):
        return self.user.username



class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    post_image = models.ImageField(upload_to="post_image",blank=False,validators=[FileExtensionValidator(['jpg', 'png'])])
    content = models.TextField()
    
    like2 = models.ManyToManyField(User, related_name='related_posts', blank=True)
    selected_at = models.DateTimeField(verbose_name="予定日", default=timezone.now)
    
    class Meta:
        ordering = ('-selected_at',)
    
    def __str__(self):
       return self.title
   
   
class Post_Mu(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    post_audio = models.FileField(upload_to="media_mp3",blank=False,validators=[FileExtensionValidator(['mp3'])])
    content = models.TextField()
    
    mylist = models.ManyToManyField(User, related_name='mylist_post', blank=True)
    like = models.ManyToManyField(User, related_name='related_post', blank=True)
    selected_at = models.DateTimeField(verbose_name="予定日", default=timezone.now)
    
    class Meta:
        ordering = ('-selected_at',)
    
    def __str__(self):
       return self.title

    def file_name(self):
        path = os.path.basename(self.post_audio.name)  # ファイル名のみ抽出
        return path