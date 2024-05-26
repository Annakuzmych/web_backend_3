
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# встановлюємо модуль налаштувань Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calculator_project.settings')

app = Celery('calculator_project')

# використання налаштувань Django для celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматичне знаходження тасків у додатках Django
app.autodiscover_tasks()

