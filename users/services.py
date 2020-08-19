from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

def chek_and_return(request):
    jwt_object      = JWTAuthentication() 
    header          = jwt_object.get_header(request)
    raw_token       = jwt_object.get_raw_token(header)
    validated_token = jwt_object.get_validated_token(raw_token)
    user            = jwt_object.get_user(validated_token)

    user = User.objects.get(username=user).id 
    data = request.data
    
    """ remember old state, set to mutable, сhange the values, set mutable flag back """
    _mutable = data._mutable
    data._mutable = True
    data['user'] = str(user) 
    data._mutable = _mutable
    # print(data)
    return data