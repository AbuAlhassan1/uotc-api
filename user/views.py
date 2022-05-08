from enum import Enum
from django.shortcuts import get_object_or_404
from ninja import Router

from user.functions import check_S_O_permition, check_token, reload_user_token
from .models import MyUser, UserPertinence
from mytoken.models import MyToken
from config.utils.schemas import AuthOut, MessageOut, UserCreate, UserIn, UserOut, UserRole, UserUpdate, UserPasswordUpdate
from .authorization import GlobalAuth, get_user_token
from django.contrib.auth import authenticate
from django.core.cache import cache

user_controller = Router(tags=['user'])

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -------------------------Create New User [Signup]---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# Create New User [Signup]
@user_controller.post('signup', response={
    400: MessageOut,
    201: MessageOut,
})
def signup(request, payload: UserCreate):
    if payload.password != payload.confirm_password:
        return 400, {'message': 'Password and Confirm Password does not match !!!'}

    try:
        is_user_exisets = MyUser.objects.get(email=payload.email)
    except MyUser.DoesNotExist:
        # Create New User
        newUser = MyUser.objects.create_user(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            username=payload.username,
            password=payload.password
        )
        new_user_pretinence = UserPertinence.objects.create(user=newUser)
        # Generate A Token
        token = get_user_token(newUser, new_user_pretinence)

        # Save The Token In Database
        MyToken.objects.create(user=newUser, token=token['access'], is_active=True)

        # Save The Token In Cache
        cache.set(newUser.id, token['access'])

        return 201, {
            'message': 'User Created Successfully !!!'
        }
    
    return 400, {
        'message': 'User already exists !!!'
    }
# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -----------------------------Signin User [Signin]---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@user_controller.post('signin', response={
    200: AuthOut,
    400: MessageOut,
})
def signin(request, payload: UserIn):
    user = authenticate(
        email = payload.email,
        password = payload.password
    )

    if not user:
        return 404, {
            'message': 'Email Or Password is incorrect !!!'
        }
    # Get The User Object
    try: u = MyUser.objects.get(email=payload.email)
    except: return {'message': 'User Not Found !!!'}
    try: u_pretinence = UserPertinence.objects.get(user=u)
    except: return {'message': 'UserPretinence Not Found !!!'}
    # Generate A Token
    token = get_user_token(user, u_pretinence)

    # Get The DB Token For This User If Its Not Saved In cache Then Save It
    db_token = MyToken.objects.get(user=u)
    # Update The Token In DataBase
    db_token.token = token['access']
    db_token.is_active = True
    db_token.save()
    # Update The Token In Cache
    cache.set(u.id, token['access'])

    return 200, {
        'token': token,
        'user': user
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------- Get User info [Me] ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# Get User info
@user_controller.get('my_info', auth = GlobalAuth(), response={
    200: UserOut,
    400: MessageOut,
})
def me(request):
    return get_object_or_404(MyUser, id=request.auth['pk'])

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ------------------------------ Update User info ----------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@user_controller.put('update_my_info', auth = GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut,
})
def update_me(request, payload: UserUpdate):
    try:
        user = get_object_or_404(MyUser, id=request.auth['pk'])
    except:
        return {
            'message': 'User Not Found !!!'
        }
    user.first_name = payload.first_name
    user.last_name = payload.last_name
    user.username = payload.username
    user.email = payload.email
    user.save()
    return 200, {
        'message': 'User info updated successfully !!!'
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------- Update User Password -------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# Update User Password
@user_controller.put('update_password', auth = GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut,
})
def update_password(request, payload: UserPasswordUpdate):
    if payload.password != payload.confirm_password:
        return 400, {
            'message': 'Password and Confirm Password does not match !!!'
        }
    try:
        user = get_object_or_404(MyUser, id=request.auth['pk'])
    except:
        return {
            'message': 'User Not Found !!!'
        }
    is_the_user = user.check_password(payload.old_password)

    if not is_the_user:
        return 400, {
            'message': 'Old password is incorrect !!!'
        }
    
    user.set_password(payload.password)
    user.save()
    return 200, {
        'message': 'Password updated successfully !!!'
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ------------------------------- Change User Role ---------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

class Role(Enum):
    st = "st"
    br = "br"
    te = "te"
    hob = "hob"
    hod = "hod"
    ad = "ad"
    su = "su"

@user_controller.put('change_user_role', auth = GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut,
})
def change_user_role(request, object_user_id: int, role: Role):
    roles = ['st', 'br', 'te', 'hob', 'hod', 'ad', 'su']
    
    subject_user = get_object_or_404(MyUser, id=request.auth['pk'])
    request_token = request.headers['Authorization'].split(' ')[1]

    if check_token(user=subject_user, request_token=request_token) != True:
        reload_user_token(user=subject_user)
    
    object_user = get_object_or_404(MyUser, id=object_user_id)
    object_user_pretinence = get_object_or_404(UserPertinence, user=object_user)

    if check_S_O_permition(s=subject_user, o=object_user) != True:
        return {
            'message': 'You Dont Have Permition !!!'
        }
    
    try:
        object_user_pretinence.role = role.value
        object_user_pretinence.save()
    except:
        return {
            'message': 'Role Not Found !!!'
        }
    return 200, {
        'message': 'Role Updated Successfully !!!'
    }

# ----------------------------------- End ------------------------------------------