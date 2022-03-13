from django import template

register = template.Library()


@register.filter
def val_ret_lstp(values, key):
    dict = {key: val for key, val in values}
    return dict.get(key)
