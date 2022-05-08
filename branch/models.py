from django.db import models
from department.models import Department

class Branch (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.title} [{self.department.title}]"