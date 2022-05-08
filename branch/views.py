from django.shortcuts import get_object_or_404, render
from ninja import Router
from branch.models import Branch
from config.utils.schemas import BranchCreate, BranchDelete, BranchOut, BranchRead, BranchUpdate, MessageOut
from department.models import Department
from user.authorization import GlobalAuth
from user.functions import check_permition
from user.models import MyUser


branch_controller = Router(tags=['branch'])

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -------------------------- Create New Branch ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@branch_controller.post('create_branch', auth=GlobalAuth(), response={
    400: MessageOut,
    201: MessageOut,
    200: MessageOut,
})
def create_branch(request, payload: BranchCreate):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
        if not payload.title and not payload.department:
            return {
                'message': "Plz Provide A Title And Department Id :) "
            }
        department = Department.objects.get(id=payload.department.id)
        if not department:
            return {
                'message': "Department Not Found !!! "
            }
        
        try:
            Branch.objects.create(title=payload.title, department=department)
        except:
            return {
                'message': "Error Occured !!! "
            }
        return 201, {
            'message': 'Branch Created Successfully !!!'
        }
    
    return {
        'message': 'Access Denied !!!'
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ---------------------------- Update A Branch ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
@branch_controller.put('update_branch', auth=GlobalAuth(), response={
    400: MessageOut,
    201: MessageOut,
    200: MessageOut,
})
def update_branch(request, payload: BranchUpdate):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
    
        if not payload.title and not payload.department:
            return {
                'message': "Plz Provide A Title And Department Id :) "
            }
        department = get_object_or_404(Department, id=payload.department.id)
        if not department:
            return {
                'message': "Department Not Found !!! "
            }
        branch = get_object_or_404(Branch, id=payload.id)
        branch.title = payload.title
        branch.department = department
        branch.save()
        return 201, {
            'message': 'Branch Updated Successfully !!!'
        }
    return {
        'message': 'Access Denied !!!'
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -------------------------- Get A Branch Info ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@branch_controller.get('get_branch', auth=GlobalAuth(), response={
    400: MessageOut,
    404: MessageOut,
    200: BranchOut,
})
def get_branch(request, payload: BranchRead):
    if request.auth['role'] == 'ad' or request.auth['role'] == 'su':
        if not payload.id:
            return {
                'message': "Plz Provide An id :) "
            }
        branch = get_object_or_404(Branch, id=payload.id)
        return 200, branch
    return {
        'message': 'Access Denied !!!'
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ---------------------------- Delete A Branch ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
@branch_controller.delete('delete_branch', auth=GlobalAuth(), response={
    400: MessageOut,
    404: MessageOut,
    200: MessageOut,
})
def delete_branch(request, payload: BranchDelete):
    user = get_object_or_404(MyUser, id= request.auth['pk'])
    if check_permition(s=user) == True:
        if not payload.id:
            return {
                'message': "Plz Provide An id :) "
            }
        branch = get_object_or_404(Branch, id=payload.id)
        branch.delete()
        return 200, {
            'message': 'Branch Deleted Successfully !!!'
        }
    return {
        'message': 'Access Denied !!!'
    }

# ----------------------------------- End ------------------------------------------