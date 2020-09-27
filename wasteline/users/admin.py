from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from wasteline.users.forms import UserChangeForm, UserCreationForm
from wasteline.users.models import Collector, CollectorMore, Customer, CustomerMore

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    pass


@admin.register(CollectorMore)
class CollectorMoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerMore)
class CustomerMoreAdmin(admin.ModelAdmin):
    pass
