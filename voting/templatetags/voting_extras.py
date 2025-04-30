# file created by Pawel Krezel (W1837610)
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)