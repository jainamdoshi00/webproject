from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=64,unique=True)
    name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    description_of_user = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

