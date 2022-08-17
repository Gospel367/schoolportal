from pyexpat import model
from django.db import models
from profiles.models import CustomUser
from django.utils.text import slugify


class TrialUser(CustomUser):
    is_admitted = models.BooleanField(default=True)
    pass