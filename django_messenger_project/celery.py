from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_messenger_project.settings')

app = Celery('django_messenger_project')

# Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматичне виявлення завдань додатках Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
