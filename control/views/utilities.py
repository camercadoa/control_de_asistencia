from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def guardar_sede(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sede_id = data.get('sede')
        if sede_id:
            request.session['sede_id'] = sede_id
            print(request.session['sede_id'])
            return JsonResponse(
                {
                    'message': 'Sede guardada exitosamente.'
                },
                status=200
            )
        return JsonResponse(
            {
                'error': 'No se envió una sede válida.'
            },
            status=400
        )
    return JsonResponse(
        {
            'error': 'Método no permitido.'
        },
        status=405
    )