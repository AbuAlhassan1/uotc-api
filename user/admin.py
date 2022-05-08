from django.contrib import admin
from user.models import MyUser, UserPertinence

admin.site.register(MyUser)
admin.site.register(UserPertinence)
