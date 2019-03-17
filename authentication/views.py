from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView,CreateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'generic_form.html'


class PasswordUpdateView(LoginRequiredMixin,SuccessMessageMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'generic_form.html'
    success_message = 'Password changed successfully!'
    success_url = 'update_password'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'user': self.request.user,
        })
        return form_kwargs
  
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return self.form_valid(form = form)
        return self.form_invalid( form = form)
