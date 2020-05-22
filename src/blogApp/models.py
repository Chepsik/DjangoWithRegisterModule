from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#external
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from colorful.fields import RGBColorField
from taggit.managers import TaggableManager

def user_directory_path(instance, filename):
    return 'public/profile_pictures/user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, unique = True)
    first_name = models.TextField(max_length = 30, blank = True)
    last_name = models.TextField(max_length = 30, blank = True)
    profile_picture = models.ImageField(upload_to = user_directory_path, blank=True)
    birth_date = models.DateField(null = True, blank = True)
    user_since = models.DateTimeField(auto_now_add = True)
    author = models.BooleanField(default = False)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' : ' + self.last_name

class Category(models.Model):
    title = models.TextField(max_length = 30)
    color = RGBColorField(default = '1183db')
    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField(max_length = 30)
    image_on_view = models.ImageField(upload_to = 'public/articles/images/%m/%d')
    text = RichTextUploadingField(blank = True)

    published = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    tags = TaggableManager(blank = True)

    visible = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = RichTextUploadingField(config_name='comments')

    published = models.DateTimeField(auto_now_add = True)

    edited = models.BooleanField(default = False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        instance.profile.save()
