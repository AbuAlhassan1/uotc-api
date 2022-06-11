from ssl import create_default_context
from django.db import models
from user.models import MyUser
from department.models import Department
from branch.models import Branch

class Post (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post/')
    auther = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    is_specific = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.auther.username} : {self.title} [{self.department.title}]"