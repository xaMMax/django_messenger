from django import template

register = template.Library()


@register.simple_tag
def has_perm(user, perm):
    return user.has_perm(perm)


@register.filter
def has_permission(user, perm):
    return user.has_perm(perm)
