from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context: dict, url_name: str, active_class: str = "active bg-primary text-white fw-semibold", inactive_class: str = "text-light text-opacity-75") -> str:
    '''
    Info:
        Retorna clases CSS condicionales basadas en la URL actual para resaltar enlaces activos.

    Params:
        context (dict): Contexto de template que contiene el objeto request.
        url_name (str): Nombre de la ruta a evaluar contra la URL actual.
        active_class (str): Clases CSS para el enlace activo.
        inactive_class (str): Clases CSS para el enlace inactivo.

    Return:
        str: Clases CSS correspondientes al estado activo o inactivo del enlace.
    '''

    # Info: Obtener objeto request desde el contexto
    request = context["request"]

    # Warn: Retornar clase activa si la URL actual coincide con el nombre de ruta
    if request.resolver_match and request.resolver_match.url_name == url_name:
        return active_class

    # Info: Retornar clase inactiva por defecto
    return inactive_class
