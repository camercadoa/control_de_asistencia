def dashboard_context(request):
    """
    Contexto global para el dashboard.
    Define variables que estarán disponibles en todos los templates.
    """
    url_name = getattr(getattr(request, "resolver_match", None), "url_name", "")

    return {
        "is_config_active": url_name in [
            "appDashboardSettingsSedesRender",
            "appDashboardSettingsAreasTrabajoRender",
        ]
    }
