from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100 , null=False , blank=False)
    description = models.TextField(max_length=250, null=True, blank=True)
    video_file = models.FileField(upload_to='video/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)



    # def __str__(self):
    #     return self.owner
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','video')

