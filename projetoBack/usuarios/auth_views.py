from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_staff': user.is_staff
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout realizado'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Erro ao fazer logout'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_tokens(request):
    all_tokens = request.data.get('all_tokens', False)
    try:
        if all_tokens:
            Token.objects.filter(user=request.user).delete()
            message = 'Todos os tokens revogados'
        else:
            request.user.auth_token.delete()
            message = 'Token atual revogado'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Erro ao revogar tokens'}, status=status.HTTP_400_BAD_REQUEST)