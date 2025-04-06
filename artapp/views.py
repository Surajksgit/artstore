from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'arthome.html')


# user login------------------------------------>

def user_login(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                user = None

        if user is not None:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('home')  # Change as needed
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "User not found.")
    
    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f"/reset-password/{uid}/{token}/"
            )

            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {reset_link}',
                'noreply@artbhavan.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset link sent to your email.')
            return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
    
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['password']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been reset. You can login now.")
            return redirect('user_login')
        return render(request, 'reset_password.html')
    else:
        messages.error(request, "Invalid or expired link.")
        return redirect('forgot_password')