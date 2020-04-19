from django.shortcuts import render, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "core/index.html")


def features(request):
    return render(request, "core/features.html")


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse("index")
