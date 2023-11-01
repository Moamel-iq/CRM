from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

app_name = 'account'


class UserManager(UserManager):
    def get_by_natural_key(self, email):
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: email})

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have an email to register')

        user = self.model(
            email=email
            , **extra_fields

        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
    )
    phone_regex = RegexValidator(
        regex=r'^(?:\+964|964)?\s?7\d{9}$',
        message="Phone number must be entered in the format: '+964 7XXXXXXXXX'."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name='Phone number',
    )
    organization_name = models.CharField(
        verbose_name=_("Organization Name"),
        max_length=50
    )
    business = models.CharField(
        verbose_name=_("Business"),
        max_length=50,
        # choices=INDUSTRYCHOICES,
        help_text=_("Select your business type:"),
        null=True, blank=True,
    )
    business_manager_name = models.CharField(
        verbose_name=_('Business Manager Name'),
        max_length=50,
        null=True, blank=True
    )
    brand_logo = models.ImageField(
        'Brand Logo',
        null=True, blank=True,
        upload_to='images/brand_logo/',
    )

    defaultURL = models.URLField(null=True, blank=True)

    otp = models.SmallIntegerField(
        help_text='One Time Password',
        null=True, blank=True
    )
    token = models.CharField(
        verbose_name=_('Token'),
        max_length=100,
        unique=True,
        null=True, blank=True, editable=False,
        help_text='Token for authentication'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        help_text='IP Address',
        blank=True, null=True
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this user has been verified.'
            'Un-verified users cannot log in.'
        ),
    )
    is_founder = models.BooleanField(
        _('founder'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as founder.'
        ),
    )
    is_ceo = models.BooleanField(
        _('ceo'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as CEO.'
        ),
    )
    is_admin = models.BooleanField(
        _('admin'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as admin.'
        ),
    )
    is_manager = models.BooleanField(
        _('manager'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as manager.'
        ),
    )
    is_hr = models.BooleanField(
        _('hr'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as Human resources (HR).'
        ),
    )
    is_accountant = models.BooleanField(
        _('accountant'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as accountant.'
        ),
    )
    is_employee = models.BooleanField(
        _('employee'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as employee.'
        ),
    )
    is_customer = models.BooleanField(
        _('customer'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as customer.'
        ),
    )
    is_supplier = models.BooleanField(
        _('supplier'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as supplier.'
        ),
    )

    # Timestamps fields
    otp_created_time = models.DateTimeField(
        default=now,
        verbose_name=_('OTP created time'),
        editable=False,
    )
    password_changes_datatime = models.DateTimeField(
        verbose_name=_('Password changes datatime'),
        blank=True,
        null=True,
    )
    last_activity = models.DateTimeField(
        verbose_name=_('Last activity'),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=now, editable=False)

    session = models.OneToOneField(Session, on_delete=models.CASCADE, blank=True, null=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
