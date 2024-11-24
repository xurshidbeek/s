from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [

    path('', views.UserListView.as_view(), name='user_list'),

    # Registration page
    path('registration/', views.RegistrationView.as_view(), name='registration'),

    # Login page
    path('login/', LoginView.as_view(template_name='app_users/user_registration.html'), name='login'),

    # Logout functionality
    path('logout/', views.logout_view, name='logout'),
]
