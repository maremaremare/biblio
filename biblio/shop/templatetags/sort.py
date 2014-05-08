from django import template
register = template.Library()


@register.filter
def author(queryset, order):
    return queryset.filter(author__slug=order)
