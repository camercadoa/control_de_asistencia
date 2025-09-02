from django import template

register = template.Library()


# Info: Template tag que retorna una clase CSS según si la URL actual coincide con `url_name`
@register.simple_tag(takes_context=True)
def active_link(context, url_name, active_class="active bg-primary text-white fw-semibold", inactive_class="text-light text-opacity-75"):
    # Params:
    #   url_name (str) -> Nombre de la ruta a evaluar
    #   active_class (str) -> Clases CSS para el link activo (default: "active bg-primary text-white fw-semibold")
    #   inactive_class (str) -> Clases CSS para el link inactivo (default: "text-light text-opacity-75")
    request = context["request"]

    # Warn: Si la URL actual coincide con `url_name`, retorna la clase activa
    if request.resolver_match and request.resolver_match.url_name == url_name:
        return active_class

    # Info: Si no coincide, retorna la clase inactiva
    return inactive_class
