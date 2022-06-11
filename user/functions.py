from user.authorization import get_user_access_token
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

# import pyrebase
# # import firebase_admin

# config = {
#   "apiKey": "AIzaSyA_meCX1wC2HPWicsdlb2L2N8IPg26pEwQ",
#   "authDomain": "uotc-4c343.firebaseapp.com",
#   "databaseURL": "https://uotc-4c343-default-rtdb.europe-west1.firebasedatabase.app/",
#   "projectId": "uotc-4c343",
#   "storageBucket": "uotc-4c343.appspot.com",
#   "messagingSenderId": "420182467743",
#   "appId": "1:420182467743:web:d05a0c278b18999bfd6eaa"
# };

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# database = firebase.database()

