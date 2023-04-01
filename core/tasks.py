import uuid
from django.contrib.auth.hashers import make_password
import re
from celery import shared_task
from .models import Accounts

@shared_task()
def change_pass_auth_scheduler():
    all_users_in_site=Accounts.objects.all()
    for user_in_site in all_users_in_site:
        user_in_site.password_auth=make_password(str(uuid.uuid4()))
        user_in_site.password_auth="".join(c for c in user_in_site.password_auth if c.isalnum())
        user_in_site.password_auth = re.sub(r'.', '', user_in_site.password_auth, count = 20)
        user_in_site.save()