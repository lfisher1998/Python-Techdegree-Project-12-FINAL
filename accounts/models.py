from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
    
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)

class Skill(models.Model):
    SKILL_CHOICES = (
        ('android', "Android Developer"),
        ('designer', "Designer"),
        ('java', "Java Developer"),
        ('php', "PHP Developer"),
        ('python', "Python Developer"),
        ('rails', "Rails Developer"),
        ('wordpress', "Wordpress Devloper"),
        ('ios', "iOS Developer")
    )
    name = models.CharField(choices=SKILL_CHOICES, max_length=50,default="")
    
    def __str__(self):
        return self.name.title()

    
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile")
    full_name = models.CharField(max_length=50)
    about = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.user.username.title()

    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    


