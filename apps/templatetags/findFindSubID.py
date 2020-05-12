



from django import template
from apps.models import *
from django.contrib.auth.models import User

register = template.Library()


def findFindSubID(user_value, plan_id):
    try:
        return subscription.objects.get(user = user_value, plan = plan.objects.get(id = plan_id)).id
    except:
        return None

register.filter(findFindSubID)