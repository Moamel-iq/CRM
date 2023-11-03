import uuid

from django.db.models import Q

from .models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm

"""Send verification token to user email"""


def sendVerifyToken(email, token, current_site):
    body = render_to_string('account/email/verify_email.html', {'domain': current_site, 'token': token, 'email': email})

    mail = EmailMessage(
        subject='Verification Needed!',
        body=body,
        # FIXME: EMAIL_BACKEND Is for testing
        from_email=settings.EMAIL_BACKEND,
        to=[email],
    )
    mail.content_subtype = 'html'
    # TODO: Recommendation is use celery for background tasks.
    mail.send()


"""Verify user token"""


def VerifyToken(request, token):
    user_profile = User.objects.filter(token=token).first()
    if user_profile.is_verified:
        messages.info(request, 'Email already verified')
        return redirect('sign-in')
    if user_profile:
        user_profile.is_verified = True
        user_profile.save()
        messages.success(request, 'Your account has been verified.')
        return redirect('success')
    else:
        messages.info(request, 'Something went worng.')


"""Sign up view"""""


def RegisterView(request):
    ''' Sign up new user to freshdesk '''
    if request.method == 'POST':
        name = request.POST.get('name')
        organization = request.POST.get('OrganizationName')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        repeatPassword = request.POST.get('RepeatPassword')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists.')
            return redirect('sign-up')

        if User.objects.filter(phone_number=phone_number).exists():
            messages.info(request, 'Mobile number already exists.')
            return redirect('sign-up')

        if password and repeatPassword:
            if password != repeatPassword:
                messages.info(request, "The two password fields didn't match.")
                return redirect('sign-up')
        print('Passed all errors')
        with transaction.atomic():
            # If something went wrong/fails
            # The database will perform a rollback by itself.
            auth_token = str(uuid.uuid4())
            user_create = User.objects.create(naem=name, organization_name=organization, phone_number=phone_number,
                                              email=email, token=auth_token)
            user_create.set_password(password)
            user_create.save()
            # to get the domain of the current site
            current_site = get_current_site(request).domain
            sendVerifyToken(email, auth_token, current_site)
            return redirect('token_send')
    return render(request, 'account/register.html')


def Tokensend(request):
    '''Let user to check there email for further instruction '''
    return render(request, 'account/token_send.html')


def Success(request):
    ''' When user successfully verify there email '''
    return render(request, 'account/success.html')


"""Sign in view"""


def SignInView(request):
    ''' Sign in views '''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            messages.info(request, '%s Not found!' % email)
            return redirect('sign-in')

        profile = User.objects.filter(email=user).first()
        ''' User verification checks '''
        if not profile.is_verified:
            messages.info(request, 'Your account is not verified!')
            return redirect('sign-in')

        auth_user = authenticate(email=email, password=password)
        if auth_user is None:
            messages.info(request, 'Wrong credentials')
            return redirect('sign-in')
        login(request, auth_user)
        return redirect('dashboard')
    return render(request, 'account/login.html')


"""Sign out view"""


class SignOutView(LoginRequiredMixin, View):
    ''' Logoutview will logout the current login user '''

    def get(self, request):
        logout(request)
        return redirect('/')


"""Password reset view"""


class PasswordResetView(View):
    '''
    Password reset with email address
    '''

    def get(self, request, *args, **kwargs):
        return render(request, 'account/password/forgot-password.html', {'form': PasswordResetForm()})

    def post(self, request, *args, **kwargs):
        ''' '''
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email_template_name = "account/password/email/password_reset_email.html"
                    current_site = Site.objects.get_current()
                    email_context = {
                        'email': user.email,
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    body = render_to_string(email_template_name, email_context)
                    email = EmailMessage(
                        subject="Password Reset Requested for your Freskdesk Account.",
                        body=body,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[user.email],
                    )
                    email.content_subtype = "HTML"
                    try:
                        EmailThread(email).start()
                        return redirect('password_reset_done')
                        messages.success(request,
                                         'A message with reset password instructions has been sent to your inbox.')
                    except Exception as e:
                        print(e)
                        messages.error(request, "Email sending failed. Please try again.")
                return redirect('dashboard')
            else:
                messages.error(request, "Email address not found.")
        return render(request, 'account/password/forgot-password.html', {'form': form})
