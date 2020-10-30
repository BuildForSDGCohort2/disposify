from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ General Model for Users
    """

    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        COLECTOR = "COLECTOR", "Collector"

    base_type = Types.CUSTOMER

    # What type of user are we?
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    is_customer = models.BooleanField(default=False)
    is_collector = models.BooleanField(default=False)

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone_number = models.CharField(max_length=255, default="No Number")
    address = models.CharField(max_length=255, default="No address")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collectors = models.ManyToManyField(User, related_name="subscribers", blank=True)


class Collector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    price_per_kg = models.FloatField(max_length=50, blank=True)
