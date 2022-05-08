from html import entities
from django.db import models
from user.models import MyUser

class Gathering (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    descriotion = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    leader = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"The leader [{self.leader.first_name}] || {self.title}"

class GatheringEntities (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    gathering = models.ForeignKey(Gathering, on_delete=models.DO_NOTHING)
    entities = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.gathering.title

class GatheringRequest (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    gathering = models.ForeignKey(Gathering, on_delete=models.DO_NOTHING)
    to = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name="to")
    From = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name="From")

    def __str__(self):
        return f"title = [{self.gathering.title}] || request from [{self.From.first_name}] to [{self.to.first_name}]"