import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "followbesideme.settings")
os.environ.setdefault('FORKED_BY_MULTIPROCESSING','1')
app = Celery("followbesideme")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_schedule = {
        'task1':{
            'task':'core.tasks.change_pass_auth_scheduler',
            'schedule': 300,
        },
   }
app.autodiscover_tasks()