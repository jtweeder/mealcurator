from math import modf
from fractions import Fraction
from django import template
from mealcurator import choices

register = template.Library()


@register.filter
def val_ret_lstp(values, key):
    dict = {key: val for key, val in values}
    return dict.get(key)


@register.filter
def dec_cleaner(qty):
    dec, num = modf(qty)
    dec = Fraction(round(dec, 3)).limit_denominator(8)
    num = int(num)
    if dec == 1:
        num += dec
        dec = 0

    if num == 0:
        out = f'{str(dec)}'
    elif dec == 0:
        out = f'{str(num)}'
    else:
        out = f'{str(num)} {str(dec)}'
    return out


@register.filter
def choice_finder(key, list):
    list = {'sections': choices.sections,
            'uoms': choices.uoms,
            }[list]
    choice_dict = {a: b for a, b in list}
    return(choice_dict[key])
