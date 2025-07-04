from rest_framework.decorators import api_view
from rest_framework.response import Response
from rareapi.models import User


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated User

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']
    user = User.objects.filter(uid=uid).first()

    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'bio': user.bio
        }
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
      '''

    user = User.objects.create(
        first_name=request.data['firstName'],
        last_name=request.data['lastName'],
        bio=request.data['bio'],
        uid=request.data['uid'],
        profile_image_url = request.data["PFP"],
        email = request.data["email"],
        active = request.data["active"],
        is_staff = request.data["isStaff"]
    )

    fullname = user.first_name + " " + user.last_name

    data = {
        'message': 'user has been registered',
        'id': user.id,
        'full name': fullname,
    }
    return Response(data)
