from django.urls import path
from . import views  # Ensure views are correctly imported

urlpatterns = [
    path('', views.home, name='arthome'),  # Example path
    path('login/', views.user_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # you’ll add this view
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('myprofile/', views.my_profile, name='my_profile'),
    
]
