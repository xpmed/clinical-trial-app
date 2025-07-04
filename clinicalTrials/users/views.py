from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
)
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

User = get_user_model()


# Logowanie
class CustomLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("dashboard")


# Aktywacja konta
class ActivateAccountView(FormView):
    """
    • link w e-mailu zawiera uidb64 i token
    • po poprawnej walidacji tokenu użytkownik ustawia hasło,
      konto staje się aktywne i następuje automatyczne zalogowanie
    """
    template_name = "auth/activate_account.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs["uidb64"]).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404(_("Nieprawidłowy link aktywacyjny."))

        if not default_token_generator.check_token(self.user, kwargs["token"]):
            raise Http404(_("Link aktywacyjny wygasł lub jest nieprawidłowy."))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        self.user.is_active = True
        self.user.save()
        login(self.request, self.user)
        return super().form_valid(form)


# Resetowanie hasła
class CustomPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset.html"
    email_template_name = "emails/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
