from django.urls import path
from . import views  # Ensure views are correctly imported

urlpatterns = [
    path('', views.home, name='arthome'),  # Example path
    
]
