from django.db import models
from user.models import MyUser

class MyToken (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Token = [{self.token}] || is_active = {self.is_active}"
