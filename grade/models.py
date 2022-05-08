from django.db import models
from subject.models import SubjectPretinence
from user.models import MyUser

class Grade (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    level = models.IntegerField()
    subject = models.ForeignKey(SubjectPretinence, on_delete=models.DO_NOTHING)
    grade = models.IntegerField()
    evaluation = models.CharField(max_length=50)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + " " + self.Subject.title + " " + str(self.grade)
    