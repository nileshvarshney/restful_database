from models.user import UserModel
from werkzeug.security import safe_str_cmp

# authenticate function
def authenticate(username, passoword):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,passoword):
        return  user

# identity  function
def identity(payload):
    """
       This function extract identity from token payload and
       map it  with the userid mapping.
       Return  : user_id if count  else return None
    """
    user_id = payload['identity'][0]
    return UserModel.find_by_id(user_id)

   


