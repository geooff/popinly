from django.shortcuts import render, reverse
from django.views.generic.edit import FormView
from .forms import RegistrationForm


def index(request):
    return render(request, "core/index.html")


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse("index")
