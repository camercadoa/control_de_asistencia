from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json, traceback

@csrf_exempt
def iniciarSesion(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({}, status=200)  # ✅ Sesión iniciada
            else:
                return JsonResponse({}, status=401)  # ❌ Credenciales inválidas

        return JsonResponse({}, status=405)  # Método no permitido

    except json.JSONDecodeError:
        return JsonResponse({}, status=400)  # JSON inválido
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({}, status=500)  # Error inesperado
