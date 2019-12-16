from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    timeline = models.CharField(max_length=200, blank=True)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Position(models.Model):
    project = models.ForeignKey(Project, related_name="positions")
    name = models.CharField(max_length=200)
    description = models.TextField()
    skill = models.ForeignKey('accounts.Skill', blank=True)
    filled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Application(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    position = models.ForeignKey(Position, related_name="application")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES, default='P')
    
    class Meta:
        ordering = ['-applied_at']
        
    def __str__(self):
        return "{}'s application to {}".format(self.applicant, self.position)
    