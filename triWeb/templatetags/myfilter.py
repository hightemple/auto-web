from django import template
register=template.Library()

@register.filter(name='get_prop')
def get_prop(dictory,key):
    return dictory.get(key)