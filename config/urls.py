from django import views
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from user.views import user_controller
from department.views import department_controller
from branch.views import branch_controller
from post.views import post_controller
from subject.views import subject_controller
from grade.views import grade_controller
from gathering.views import gathering_controller
from mytoken.views import mytoken_controller

api = NinjaAPI()
api.add_router("user", user_controller)
api.add_router("department", department_controller)
api.add_router("branch", branch_controller)
api.add_router("post", post_controller)
api.add_router("subject", subject_controller)
api.add_router("grade", grade_controller)
api.add_router("gathering", gathering_controller)
api.add_router("mytoken", mytoken_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), 
]
