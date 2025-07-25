import json
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'is_staff': user.is_staff
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)