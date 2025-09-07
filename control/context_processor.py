def dashboard_context(request):
    # Info: Contexto global para el dashboard.
    #       Define variables que estarán disponibles en todos los templates.
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Info: Obtener el nombre de la URL actual
    url_name = getattr(getattr(request, "resolver_match", None), "url_name", "")

    # Info: Diccionario con los menús y sus URLs asociados
    menu_groups = {
        "config": [
            "appDashboardLocationSettingsRender",
            "appDashboardWorkAreaSettingsRender",
        ],
        "employees": [
            "appDashboardActiveEmployeesRender",
            "appDashboardInactiveEmployeesRender",
        ],
    }

    # Info: Construir un diccionario dinámico de flags
    active_menus = {f"is_{menu}_active": url_name in urls for menu, urls in menu_groups.items()}

    # Return: Diccionario con menús activos
    return active_menus
