import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from control.models import (
    Empleado, Sede
)

def saveRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        fechaHoraRegistro = data.get('fechaHoraRegistro')
        sede_id = request.session.get('sede_id')
        sede = get_object_or_404(Sede, id=sede_id)

        if not codigo:
            return JsonResponse({'warning': 'Código no proporcionado'}, status=400)

        try:
            # Validar que el código corresponde a un empleado registrado
            empleado = Empleado.objects.get(numero_documento=codigo)

            # Preparar la información para la respuesta
            empleado_info = {
                'nombre_completo': f"{empleado.primer_nombre.upper()} {empleado.primer_apellido.upper()}",
                'cargo': empleado.cargo.upper(),
                'hora_registro': fechaHoraRegistro
            }

            print(empleado_info)
            print(f'{sede.ubicacion} - {sede.ciudad}')
            return JsonResponse({'success': True, 'empleado': empleado_info})
        except Empleado.DoesNotExist:
            return JsonResponse({'error': f'Empleado no encontrado - {codigo}'}, status=404)
        except Exception as e:
            return JsonResponse({'warning': 'Código no válido - Solo valores numéricos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)