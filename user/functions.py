from ast import Return
from mytoken.models import MyToken
from user.authorization import get_user_token
from user.models import MyUser, UserPertinence


def check_S_O_permition(s: MyUser, o: MyUser):
    roles = ['st', 'br', 'te', 'hob', 'hod', 'ad', 'su']
    try: subject_user_permitions = UserPertinence.objects.get(user=s)
    except: 
        return False

    try: object_user_permitions = UserPertinence.objects.get(user=o)
    except: return False
    
    s_branch = subject_user_permitions.branch
    s_department = subject_user_permitions.department
    o_branch = object_user_permitions.branch
    o_department = object_user_permitions.department
    
    if s_branch == None and o_branch == None:
        if s_department == None and o_department == None:
            return False
    if roles.index(subject_user_permitions.role) <= roles.index(object_user_permitions.role):
        return False
    
    if subject_user_permitions.role == 'br' or subject_user_permitions.role == 'te':
        return False

    if s_branch == None:
        if o_branch == None:
            return False
        if s_department == o_department:
            return False
        
        return False
    
    if s_branch == o_branch:
        return True
    if s_department == o_department:
        return True
    
    return False

def check_permition(s: MyUser):
    roles = ['st', 'br', 'te', 'hob', 'hod', 'ad', 'su']
    try:
        user_permitions = UserPertinence.objects.get(user=s)
    except:
        return False
    
    if roles.index(user_permitions.role) <= roles.index('te'):
        return False
    
    return True

def check_token(user: MyUser, request_token: str):
    try: db_token = MyToken.objects.get(user=user)
    except: return False

    if db_token.token != request_token:
        return False
    
    return True

def reload_user_token(user: MyUser):
    try: db_token = MyToken.objects.get(user=user)
    except:
        user_pretinence = UserPertinence.objects.get(user=user)
        db_token = MyToken.objects.create(user=user, user_pretinence=user_pretinence)

    user_pretinence = UserPertinence.objects.get(user=user)
    db_token.token = get_user_token(user=user, user_pretinence=user_pretinence)
    db_token.save()

