from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from wasteline.users.models import User


class CollectorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_collector = True
        user.save()
        return user
