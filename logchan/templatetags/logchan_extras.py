from django import template
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
        return group in user.groups.all()
    except ObjectDoesNotExist:
        return False
