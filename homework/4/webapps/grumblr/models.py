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
    user  = models.OneToOneField(User)
    motto  = models.CharField(max_length=256)
    fullname = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    phone  = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    id_picture = models.ImageField(upload_to="grumblr_id_photos", blank=True)
    def __unicode__(self):
        return self.fullname

class Comment(models.Model):
    content = models.CharField(max_length=256)
    user    = models.ForeignKey(User)
    post    = models.ForeignKey(Post)
    def __unicode__(self):
        return self.content

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name="follower")
    following = models.ForeignKey(User, related_name="following")
    def __unicode__(self):
        return self.follower.id

class DislikeGrumbl(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    def __unicode__(self):
        return self.post.text


class BlockUser(models.Model):
    blocked_user = models.ForeignKey(User,related_name="blocked")
    blocking_user = models.ForeignKey(User,related_name="blocker")
    def __unicode__(self):
        return "BlockModel"
