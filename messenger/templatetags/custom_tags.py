from django import template

register = template.Library()


@register.simple_tag
def has_perm(user, perm):
    return user.has_perm(perm)


@register.filter
def has_permission(user, perm):
    return user.has_perm(perm)

@register.filter
def compare_datas(date1, date2):
    date1_truncated = date1.replace(microsecond=0)
    date2_truncated = date2.replace(microsecond=0)
    return date1_truncated != date2_truncated