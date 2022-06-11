from html import entities
from django.db import models
from user.models import MyUser

class Gathering (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    descriotion = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    leader = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='gathering_leader', blank=True)

    def __str__(self):
        return f"The leader [{self.leader.first_name}] || {self.title}"

class GatheringEntities (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    gathering = models.ForeignKey(Gathering, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    entities = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.gathering.title

class GatheringRequest (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    gathering = models.ForeignKey(Gathering, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    to = models.ForeignKey(MyUser, on_delete=models.SET_NULL, related_name="to", null=True, blank=True)
    From = models.ForeignKey(MyUser, on_delete=models.SET_NULL, related_name="From", null=True, blank=True)

    def __str__(self):
        return f"title = [{self.gathering.title}] || request from [{self.From.first_name}] to [{self.to.first_name}]"