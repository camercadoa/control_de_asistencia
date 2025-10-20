from typing import Dict
from django.http import HttpRequest


def dashboard_context(request: HttpRequest) -> Dict[str, bool]:
    '''
    Info:
        Proporciona contexto global para el dashboard, definiendo variables disponibles
        en todos los templates. Identifica qué menú está activo basado en la URL actual.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        Dict[str, bool]: Diccionario con flags booleanos indicando qué menús están activos.
        (Ejemplo: {"is_config_active": True, "is_employees_active": False})
    '''

    # Info: Obtener el nombre de la URL actual desde resolver_match
    url_name = getattr(
        getattr(request, "resolver_match", None), "url_name", "")

    # Info: Definir grupos de menús y sus URLs asociadas
    menu_groups = {
        "config": [
            "appDashboardLocationSettingsRender",
            "appDashboardWorkAreaSettingsRender",
            "appDashboardSchedulesSettingsRender",
            "appDashboardTypeNewsSettingsRender",
        ],
        "employees": [
            "appDashboardActiveEmployeesRender",
            "appDashboardInactiveEmployeesRender",
        ],
    }

    # Info: Generar flags dinámicos indicando si cada menú está activo
    active_menus = {
        f"is_{menu}_active": url_name in urls for menu, urls in menu_groups.items()}

    return active_menus
