from django.urls import path
from .views import (
    registration_api_view,
    login_api_view,
    confirm_sms_api_view
)

urlpatterns = {
    path('register/', registration_api_view, name='register'),
    path('login/', login_api_view, name='login'),
    path('confirm-sms/', confirm_sms_api_view, name='confirm_sms'),
}