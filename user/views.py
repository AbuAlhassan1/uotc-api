from enum import Enum
from django.shortcuts import get_object_or_404
from ninja import Router

from user.functions import check_S_O_permition
from .models import MyUser, UserPertinence
from config.utils.schemas import AuthOut, MessageOut, TokenRes, UserCreate, UserIn, UserOut, UserRole, UserUpdate, UserPasswordUpdate
from .authorization import GlobalAuth, get_user_access_token, get_user_refresh_token
from django.contrib.auth import authenticate
from django.core.cache import cache
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from django.core.mail import send_mail


user_controller = Router(tags=['user'])

# ----------------------------------------------------------------------------------
# -------------------------Create New User [Signup]---------------------------------
# ----------------------------------------------------------------------------------
# Create New User [Signup]
@user_controller.post('signup', response={
    400: MessageOut,
    200: MessageOut,
    201: TokenRes,
})
def signup(request, payload: UserCreate):
    if len(payload.username) < 1:
        return {'message': 'Username Is Required'}
    if not payload.email:
        return {'message': 'Email Is Required'}
    try:
        is_username_exisets = MyUser.objects.get(username=payload.username)
    except MyUser.DoesNotExist:
        try:
            is_user_exisets = MyUser.objects.get(email__exact=payload.email)

        except MyUser.DoesNotExist:
            # Create New User
            try:
                newUser = MyUser.objects.create_user(
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                    email=payload.email,
                    username=payload.username,
                    password=payload.password
                )
            except: return {"message": "Somthing Went Wrong"}
            
            try: send_mail(
                'Subject here',
                'Here is the message.',
                'qweqaz157@gmail.com',
                [payload.email],
                fail_silently=False,
            )
                    
            except Exception as e: return {'message': str(e)}


            try: new_user_pretinence = UserPertinence.objects.create(user=newUser)
            except: return {"message": "Somthing Went Wrong"}

            # Generate A Token
            access_token = get_user_access_token(newUser, new_user_pretinence)
            refresh_token = get_user_refresh_token(newUser)
            
            return 201, {
                'message': "Account Created Successfully",
                'access_token': access_token['access'],
                'refresh_token': refresh_token['refresh'],
                'user': newUser
            }
        return 400, {
            'message': 'Email Already Exists'
        }

    return {
            'message' : 'Username Already Exists'
        }

# ----------------------------------- End ------------------------------------------

@user_controller.delete("delete-user", response={
    200: MessageOut,
    400: MessageOut,
    401: MessageOut,
    403: MessageOut,
    404: MessageOut,
    500: MessageOut,
})
def delete_user(request, id):
    MyUser.objects.get(id=id).delete()

# ----------------------------------------------------------------------------------
# -----------------------------Signin User [Signin]---------------------------------
# ----------------------------------------------------------------------------------

@user_controller.post('signin', response={
    200: TokenRes,
    400: MessageOut,
})
def signin_password(request, payload: UserIn):
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
    access_token = get_user_access_token(user, u_pretinence)
    refresh_token = get_user_refresh_token(user)

    # Get The DB Token For This User If Its Not Saved In cache Then Save It
    # db_token = MyToken.objects.get(user=u)
    # Update The Token In DataBase
    # db_token.token = access_token['access']
    # db_token.is_active = True
    # db_token.save()
    # Update The Token In Cache
    # cache.set(u.id, access_token['access'])

    return 200, {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user
    }

# ----------------------------------- End ------------------------------------------

# ----------------------------------------------------------------------------------
# ----------------------------- Get User info [Me] ---------------------------------
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
# ------------------------------ Update User info ----------------------------------
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
# ----------------------------- Update User Password -------------------------------
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
# ------------------------------- Change User Role ---------------------------------
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