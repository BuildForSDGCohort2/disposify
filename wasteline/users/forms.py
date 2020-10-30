from django import forms as d_forms
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm


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


class WastelineSignUpForm(SignupForm):

    type = d_forms.ChoiceField(
        choices=[("customer", "CUSTOMER"), ("collector", "COLLECTOR")]
    )

    # Override the init method
    def __init__(self, *args, **kwargs):
        # Call the init of the parent class
        super().__init__(*args, **kwargs)
        # Remove autofocus because it is in the wrong place
        del self.fields["username"].widget.attrs["autofocus"]

    # Custom signup logic
    def custom_signup(self, request, user):
        # Set the user's type from the form response
        user.type = self.cleaned_data["type"]
        # Save the user's type to their database record
        user.save()
