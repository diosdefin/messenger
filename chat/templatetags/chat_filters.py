from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Разделяет строку по разделителю и возвращает список"""
    if value:
        return value.split(delimiter)
    return []