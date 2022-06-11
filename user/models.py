from email.mime import image
from email.policy import default
from sre_constants import BRANCH
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from branch.models import Branch

from department.models import Department

class MyUserManager(UserManager):
    def create_user(self, username, email, password, firstname=None, lastname=None):
        if not email:
            raise ValueError('Users must have an email address !!')
        elif not password:
            raise ValueError('Users must have a password !!')
        
        user = self.model()
        user.username = username
        user.email = self.normalize_email(email)
        user.first_name = firstname
        user.last_name = lastname
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, username="", firstname=None, lastname=None):
        if not email:
            raise ValueError('Users must have an email address !!')
        elif not password:
            raise ValueError('Users must have a password !!')
        
        superuser = self.model(username=username, email=email, first_name=firstname, last_name=lastname)
        superuser.set_password(password)
        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser

class MyUser (AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = MyUserManager()
    
    def __str__(self):
        return self.email + " " + str(self.id)

class Friend (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    friend = models.ForeignKey(MyUser, related_name='friends', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email + ' ' + self.friend.email

class UserPertinence (models.Model):

    role_choices = [
        ('st', 'student'),
        ('br', 'branchRepresentative'),
        ('te', 'teacher'),
        ('hob', 'headOfBranch'),
        ('hod', 'headOfDepartment'),
        ('ad', 'admin'),
        ('su', 'superuser'),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    role = models.CharField(max_length=3, choices=role_choices, default='st')

    def __str__(self):
        return f"{None if self.user == None else self.user.email} || {None if self.department == None else self.department.title} || {None if self.branch == None else self.branch.title } || {self.role}"

class HOB (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{self.user.first_name} Head Of [{self.branch.title}]"

class HOD (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    Department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{self.user.first_name} Head Of [{self.branch.title}]"

class BranchRepresentative (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} Representative Of [{self.branch.title}]"
