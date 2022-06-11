import email
from ninja import Schema

# User Schemas -- Start --
class MessageOut (Schema):
    message: str

class UserCreate (Schema):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class UserUpdate (Schema):
    first_name: str
    last_name: str
    username: str
    email: str

class UserPasswordUpdate (Schema):
    old_password: str
    password: str
    confirm_password: str

class UserIn (Schema):
    email: str
    password: str

class UserOut (Schema):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str

class UserRole (Schema):
    user_id: str
    role: str
    role: str

class UserPretinence (Schema):
    department: str
    branch: str

class RelatedUser (Schema):
    first_name: str
    last_name: str
    email: str
    user_pertinence: UserPretinence
# User Schemas -- End --

# -----------------------------------

# Token Schemas -- Start --
class TokenOut (Schema):
    access: str

class AuthOut (Schema):
    token: TokenOut
    user: UserOut

class TokenRes (Schema):
    message: str
    access_token: str
    refresh_token: str
    user: UserOut
# Token Schemas -- End --

# -----------------------------------
# Department Schemas -- Strat --
class DepartmentCreate (Schema):
    title: str

class DepartmentOut (Schema):
    title: str

class DepartmentUpdate (Schema):
    id: int
    title: str

class DepartmentRead (Schema):
    id: int

class DepartmentDelete (Schema):
    id: int
# Department Schemas -- End --

# Branch Schemas -- Strat --
class BranchCreate (Schema):
    title: str
    department: DepartmentRead

class BranchOut (Schema):
    title: str
    department: DepartmentOut

class BranchUpdate (Schema):
    id: int
    title: str
    department: DepartmentRead

class BranchRead (Schema):
    id: int

class BranchDelete (Schema):
    id: int
# Department Schemas -- End --

# Subject Schemas -- Strat --
class SubjectSchema (Schema):
    title: str

class SubjectPretinenceIn (Schema):
    subject: SubjectSchema
    department: DepartmentRead
    branch: BranchRead
# Subject Schemas -- End --