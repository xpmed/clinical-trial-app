from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    USER_ROLE_CHOICES = [
        ('administrator', _('Administrator')),
        ('researcher', _('Badacz')),
        ('doctor', _('Lekarz')),
        ('patient', _('Pacjent'))
    ]

    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, default='patient', verbose_name=_('Rola użytkownika'))
    language = models.CharField(max_length=10, default='pl', choices=[('pl', 'Polski'), ('en', 'English')], verbose_name=_('Język'))

    class Meta:
        verbose_name = _('Użytkownik')
        verbose_name_plural = _('Użytkownicy')
        

    def __str__(self):
        return self.username
