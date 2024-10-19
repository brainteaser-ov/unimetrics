from django import template

register = template.Library()


@register.filter
def ru_pluralize(value, arg=""):
    args = arg.split(",")
    try:
        number = abs(int(value))
    except (ValueError, TypeError):
        number = 0
    if len(args) < 3:
        args = ["", "", ""]

    if number % 10 == 1 and number % 100 != 11:
        return args[0]
    elif 2 <= number % 10 <= 4 and not (12 <= number % 100 <= 14):
        return args[1]
    else:
        return args[2]
