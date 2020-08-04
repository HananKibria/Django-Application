# from django.db import models
# import datetime
# from django.utils import timezone
# # Create your models here.
#
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="", null=True)
    tags = ArrayField(models.CharField(max_length=255, unique=False,
                                       blank=True), unique=False, blank=True,
                      default=list)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.titl