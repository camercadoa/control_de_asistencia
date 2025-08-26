import json
from django.http import JsonResponse
from control.models import (
    Empleado, RegistroAsistencia
)
from django.utils.timezone import now

def GuardarRegistro(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')

        if not codigo:
            return JsonResponse({'error': 'Código no proporcionado'}, status=400)

        try:
            # Validar que el código corresponde a un empleado registrado
            empleado = Empleado.objects.get(numero_documento=codigo)

            # Preparar la información para la respuesta
            empleado_info = {
                'nombre_completo': f"{empleado.primer_nombre} {empleado.primer_apellido}",
                'cargo': empleado.cargo,
                'hora_registro': now().strftime('%H:%M:%S'),
                'sede': request.session.get('sede_id')
            }

            return JsonResponse({'success': True, 'empleado': empleado_info})
        except Empleado.DoesNotExist:
            return JsonResponse({'error': f'Empleado no encontrado - {codigo}'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)