from django.db import models
from branch.models import Branch

from department.models import Department

class Subject (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class SubjectPretinence (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.subject.title + ' ' + self.department.title + ' ' + self.branch.title