from django.db import models
from teams.models import Team

# Create your models here.
class Boardmodel(models.Model):
    choice = (
        ('open','open'),
        ('inprogress','inprogress'),
        ('closed','closed'),
    )
    boardname = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    creationtime = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team,help_text='Select team for this project', on_delete=models.CASCADE)
    status = models.CharField(max_length=15 ,choices=choice, default='OPEN')

    class Meta:
        verbose_name_plural = 'BoardModel'

    def _str_(self) -> str:
        return self.name

class TaskModel(models.Model):
    choice = (
        ('open','open'),
        ('inprogress','inprogress'),
        ('complete','complete'),
    )
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    user_id = models.ForeignKey(Team, help_text="Select the team for the task", on_delete=models.CASCADE)
    creationtime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15 ,choices=choice, default='OPEN')

    class Meta:
        verbose_name_plural = 'TaskModel'

    def _str_(self) -> str:
        return self.title