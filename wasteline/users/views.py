from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from .models import Collector
from .forms import UserEditForm, CustomerEditForm, CollectorEditForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


@login_required
def user_profile_update(request):
    print(request.user)
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if request.user.type == "CUSTOMER":
            profile_form = CustomerEditForm(
                instance=request.user, data=request.POST, files=request.FILES
            )
        else:
            profile_form = CollectorEditForm(
                instance=request.user, data=request.POST, files=request.FILES
            )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        if request.user.type == "CUSTOMER":
            profile_form = CustomerEditForm()
        else:
            profile_form = CollectorEditForm()
    return render(
        request,
        "users/update.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def collector_list(request):
    collectors = Collector.objects.all()
    return render(request, "users/collector_list.html", {"collectors": collectors},)
