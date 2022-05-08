from ninja import Router
from branch.models import Branch
from config.utils.schemas import MessageOut, SubjectSchema, SubjectPretinenceIn
from department.models import Department
from subject.models import SubjectPretinence, Subject
from django.shortcuts import get_object_or_404

from user.authorization import GlobalAuth

subject_controller = Router(tags=['subject'])

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ---------------------------- Create New Subject ----------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
@subject_controller.post('create_subject', auth=GlobalAuth(), response={
    200: MessageOut,
    201: MessageOut,
    400: MessageOut,
})
def create_subject(request, payload: SubjectSchema):
    print(request.headers)
    if request.auth['role'] == 'ad' or request.auth['role'] == 'su':
        is_subject_exist = Subject.objects.filter(title=payload.title)
        if not is_subject_exist:
            Subject.objects.create(title=payload.title)
            return 201, {
                'message': 'Subject Created Successfully !!',
            }
        return {
            'message': 'Subject Already Exist !!',
        }
        
    return {
            'message': 'Access Denied !!',
    }

# ----------------------------------- End ------------------------------------------