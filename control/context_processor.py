def dashboard_context(request):
    """
    Contexto global para el dashboard.
    Define variables que estarán disponibles en todos los templates.
    """
    url_name = getattr(getattr(request, "resolver_match", None), "url_name", "")

    # Diccionario con los menús y sus URLs asociados
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

    # Construir un diccionario dinámico de flags
    active_menus = {f"is_{menu}_active": url_name in urls for menu, urls in menu_groups.items()}

    return active_menus
