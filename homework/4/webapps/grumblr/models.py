from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text

class Profile(models.Model):
    email = models.CharField(max_length=256)
    age   = models.CharField(max_length=3)
    user  = models.ForeignKey(User)
    motto  = models.CharField(max_length=256)
    fullname = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    phone  = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    def __unicode__(self):
        return self.text

class Comment(models.Model):
    content = models.CharField(max_length=256)
    user    = models.ForeignKey(User)
    post    = models.ForeignKey(Post)
    def __unicode__(self):
        return self.text
