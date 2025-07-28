from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return JsonResponse({
        'message': 'Token funcionando!',
        'user': request.user.username,
        'user_id': request.user.id,
        'is_staff': request.user.is_staff
    })