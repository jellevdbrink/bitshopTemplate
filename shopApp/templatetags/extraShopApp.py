from django import template

register = template.Library()


@register.filter
def contains_key(your_object, the_property):
    if str(the_property) in your_object.keys():
        return True
    else:
        return False


@register.filter
def contains_key_cart(cart, prod_id):
    for key in cart.keys():
        if str(prod_id) in key:
            return True
    return False


@register.filter
def second_from_split_(string):
    return string.split('_')[1]


@register.simple_tag
def get_double_object_property(your_object, first_property, second_property):
    return your_object[str(first_property)][str(second_property)]


@register.simple_tag
def get_total_amount(cart, prod):
    tot_aantal = 0
    for key, value in cart.items():
        if str(prod.id) in key:
            tot_aantal += value['aantal']

    return str(tot_aantal * prod.hoeveelheid)


@register.simple_tag
def get_total_amount_optie(cart, prod, extra_optie):
    if not extra_optie:
        return get_total_amount(cart, prod)

    the_key = str(prod.id) + '_' + extra_optie
    for key, value in cart.items():
        if key == the_key:
            return str(value['aantal'] * prod.hoeveelheid)

