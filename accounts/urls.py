from django.urls import path
from .views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', LoginView.as_view(), name='signup'),
]
