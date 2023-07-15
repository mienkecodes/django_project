from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


# can add avatars or link to urls for user, when user last logged in etc

# # Not much code, right? We're creating the simplest possible custom user, so thatwe can demonstrate how, and let you add to it later if you want to.We're subclassing from one of the built-in user models that Django includes out-of-the-box, so there are a bunch of fields built in. Take a look at the Django docs tosee what we are building on top of
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.models.AbstractUser