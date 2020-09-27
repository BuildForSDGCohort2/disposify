from django import forms as d_forms
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CollectorMore, CustomerMore

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserEditForm(d_forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "phone_number", "address")


class CollectorEditForm(d_forms.ModelForm):
    class Meta:
        model = CollectorMore
        fields = ("description", "price_per_kg")


class CustomerEditForm(d_forms.ModelForm):
    class Meta:
        model = CustomerMore
        fields = ()
