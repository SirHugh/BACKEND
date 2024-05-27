from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from .models import Periodo

# @receiver(post_save, sender=Periodo)
# def set_inactive_if_end_date_passed(sender, instance, **kwargs):
#     if instance.es_activo and instance.end_date < datetime.now():
#         instance.es_activo = False
#         instance.save()