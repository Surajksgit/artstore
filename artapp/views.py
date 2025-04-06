from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .models import UserDashboard


# Create your views here.
def home(request):
    return render(request, 'arthome.html')


# user login------------------------------------>

def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Try to get user by username or email
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                user = None

        if user is not None:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)

                # Create dashboard profile if not exists
                UserDashboard.objects.get_or_create(user=authenticated_user)

                messages.success(request, "Login successful!")
                return redirect('user_dashboard')  # Update with your actual dashboard URL name
            else:
                messages.error(request, "Invalid password. Please try again.")
        else:
            messages.error(request, "User not found. Please check your email or username.")
    
    return render(request, 'login.html')  # Your login template

# user dashboard-------------------------------->
@login_required
def user_dashboard(request):
    dashboard = UserDashboard.objects.get(user=request.user)
    return render(request, 'userdashboard.html', {'dashboard': dashboard})


# forgot password-------------------------------->
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


# reset password--------------------------------->
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
    
# user dashboard-------------------------------->
def user_dashboard(request):
    return render(request, 'userdashboard.html')

# my profile------------------------------------>
@login_required
def my_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')  # or wherever you want to redirect
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'myprofile.html', {
        'form': form,
        'user_email': user.email,
        'member_since': user.date_joined,
        'profile_initial': user.username[0].upper(),
    })