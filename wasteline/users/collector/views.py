from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import CollectorSignUpForm
from ..models import User


class CollectorSignUpView(CreateView):
    model = User
    form_class = CollectorSignUpForm
    template_name = "registration/collector_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "collector"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")
