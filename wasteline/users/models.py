from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ General Model for Users
    """

    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        COLLECTOR = "COLLECTOR", "Collector"

    base_type = Types.CUSTOMER

    # What type of user are you?
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone_number = models.CharField(max_length=255, default="No Number")
    address = models.CharField(max_length=255, default="No address")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class CustomerManager(models.Manager):
    """Manager returns only Customers
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class CollectorManager(models.Manager):
    """Manager returns only Collectors
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COLLECTOR)


class CollectorMore(models.Model):
    """Custom data fields for collectors
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    price_per_kg = models.FloatField(max_length=50, blank=True)


class Collector(User):
    """Model for Collectors
    """

    base_type = User.Types.COLLECTOR
    objects = CollectorManager()

    @property
    def more(self):
        return self.collectormore

    class Meta:
        proxy = True


class CustomerMore(models.Model):
    """Custom data fields for customers
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collectors = models.ManyToManyField(
        Collector, related_name="subscribers", blank=True
    )


class Customer(User):
    """Model for Customer
    """

    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    @property
    def more(self):
        return self.customermore

    class Meta:
        proxy = True
