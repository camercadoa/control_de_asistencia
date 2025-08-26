from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, traceback

@csrf_exempt
def GuardarSede(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            sede_id = data.get('sede')

            if sede_id:
                request.session['sede_id'] = sede_id
                return JsonResponse({}, status=200)  # Success

            return JsonResponse({}, status=400)  # Error: parámetro enviado no válido

        return JsonResponse({}, status=405)  # Método no permitido

    except json.JSONDecodeError:
        return JsonResponse({}, status=400)

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({}, status=500)  # Error inesperado en el servidor
