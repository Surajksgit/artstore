from django.urls import path
from . import views  # Ensure views are correctly imported

urlpatterns = [
    path('', views.home, name='arthome'),  # Example path
    path('login/', views.user_login, name='user_login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # you’ll add this view
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    
]
