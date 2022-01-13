from django import template

register = template.Library()


@register.filter
def contains_key(your_object, the_property):
    if str(the_property) in your_object.keys():
        return True
    else:
        return False


@register.simple_tag
def get_double_object_property(your_object, first_property, second_property):
    return your_object[str(first_property)][str(second_property)]


@register.simple_tag
def get_total_amount(cart, prod):
    return str(cart[str(prod.id)]['aantal'] * prod.hoeveelheid)
