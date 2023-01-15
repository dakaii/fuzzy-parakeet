from core.accounts.models.abstracts import TimeRecordMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountOwnerManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create a user with the given email and password."""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a super user with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class AccountOwner(AbstractUser, TimeRecordMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(), MinLengthValidator(1)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)

    objects = AccountOwnerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('account_owner')
        verbose_name_plural = _('account_owners')
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return f'{self.__class__.__name__}: [{self.email}]'