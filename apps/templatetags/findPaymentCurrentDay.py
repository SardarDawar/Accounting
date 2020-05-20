


from django import template
from apps.models import *
from django.contrib.auth.models import User

from datetime import datetime
from datetime import timedelta
register = template.Library()


def findPaymentCurrentDay(date_vaue):
    # return (datetime.now() + timedelta(days = 30)).strftime("%B")
    try:
        day = date_vaue.split("/")[1]
        return day
    except :
        day = date_vaue
        return day


register.filter(findPaymentCurrentDay)