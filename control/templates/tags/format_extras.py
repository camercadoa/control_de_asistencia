from django import template

register = template.Library()

@register.filter
def contabilidad_co(value):
    try:
        return "$ {:,.0f}".format(value).replace(",", ".")
    except:
        return value

@register.filter
def miles_co(value):
    try:
        return "{:,.0f}".format(value).replace(",", ".")
    except:
        return value

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)