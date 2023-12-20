from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Projects(models.Model):
    project_title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    project_feature = models.TextField()
    file_type = models.CharField(max_length=255, default='json', blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_title