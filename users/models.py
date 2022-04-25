from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField


class User(models.Model):
    phone_regex = RegexValidator(regex=r'^01[0125][0-9]{8}$', message="Invalid Phone Number.")
    password_regex = \
        RegexValidator(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z\d@$.!%*#?&]',
                       message="Password must be combination of Uppercase, Lowercase, Special Characters and Digits.")

    # mandatory fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(validators=[password_regex], max_length=32)
    mobile_phone = models.CharField(validators=[phone_regex], max_length=11)
    profile_picture = models.ImageField(upload_to="users/static/images")

    # optional fields
    birthday = models.DateField(null=True, blank=True)
    fb_profile = models.URLField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("user_profile", args=[self.id])
