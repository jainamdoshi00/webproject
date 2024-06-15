from django.db import models
from users.models import Users

# Create your models here.
class Team(models.Model):
    teamname = models.CharField(max_length=64,unique=True)
    description = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Users,related_name='admin',on_delete=models.CASCADE,to_field="id")
    members = models.ManyToManyField(Users,max_length=50)

    class Meta:
        verbose_name_plural = 'Team'

    def __str__(self):
        return self.teamname
    def display_members(self):
        return ', '.join(self.members.name for self.members in self.members.all()[:])
    display_members.short_description = 'Users'