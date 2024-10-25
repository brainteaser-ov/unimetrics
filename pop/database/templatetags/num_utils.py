from django import template

register = template.Library()



@register.filter
def ru_pluralize(value, arg):
    variants = arg.split(',')
    number = abs(int(value))
    if number % 10 == 1 and number % 100 != 11:
        return variants[0]
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return variants[1]
    else:
        return variants[2]

