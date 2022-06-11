from turtle import title
from django.db import models
from ckeditor.fields import RichTextField

class Department (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title + " " + str(self.id)