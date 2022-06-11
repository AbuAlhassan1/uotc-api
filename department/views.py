from lib2to3.pgen2 import token
from turtle import title
from django.shortcuts import get_object_or_404
from ninja import Router
from user.authorization import GlobalAuth
from django.core.cache import cache
from user.functions import check_permition
from user.models import MyUser
from .models import Department 
from config.utils.schemas import DepartmentDelete, DepartmentOut, DepartmentRead, MessageOut, DepartmentCreate, DepartmentUpdate

department_controller = Router(tags=['department'])

# ----------------------------------------------------------------------------------
# -------------------------- Create New Department ---------------------------------
# ----------------------------------------------------------------------------------

@department_controller.post('create_department', auth=GlobalAuth(), response={
    400: MessageOut,
    404: MessageOut,
    201: MessageOut,
    200: MessageOut,
})
def create_department(request, payload: DepartmentCreate):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
        try: Department.objects.create(title=payload.title)
        except: return {'message': 'Something Went Wrong While Creating New Department !!!'}
        return { 'message': 'Department Created Successfully !!!' }
    return {
        'message': "Access Denied !!"
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ---------------------------- Update A Department ---------------------------------
# ----------------------------------------------------------------------------------

@department_controller.put('update_department', auth=GlobalAuth(), response={
    400: MessageOut,
    201: MessageOut,
    200: MessageOut,
})
def update_department(request, payload: DepartmentUpdate):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
        try: department = get_object_or_404(Department, id=payload.id)
        except: return {'message': 'Department Not Found !!!'}
        department.title = payload.title
        department.save()
        return {
            'message': "Department Updated Successfully !!!",
        }
    return {
        'message': "Access Denied !!"
    }
# ----------------------------------- End ------------------------------------------


# ----------------------------------------------------------------------------------
# -------------------------- Get A Department Info ---------------------------------
# ----------------------------------------------------------------------------------

@department_controller.get('get_department', response={
    400: MessageOut,
    404: MessageOut,
    200: DepartmentOut,
})
def get_department(request, id: int):
    department = Department.objects.get(id=id)
    return {
        'title': department.title,
    }
# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ---------------------------- Delete A Department ---------------------------------
# ----------------------------------------------------------------------------------

@department_controller.delete('delete_department', auth=GlobalAuth(), response={
    400: MessageOut,
    404: MessageOut,
    200: MessageOut,
})
def delete_department(request, payload: DepartmentDelete):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
        try: department = get_object_or_404(Department, id=payload.id)
        except: return {'message': 'Department Not Found !!!'}
        department.delete()
        return {
            'message': "Department Deleted Successfully !!!",
        }
    return {
        'message': "Access Denied !!"
    }

# ----------------------------------- End ------------------------------------------