from django.urls import path
from . import views

urlpatterns = [
    # Authentication-related paths
    path('', views.login_page, name="login_page"),  # Default to login page
    path('register/', views.register, name="register"),
    path('logout/', views.log_out, name='log_out'),

    # Employee management paths
    path('index/', views.index, name="index"),  # Replacing 'home' with 'index'
    path('add_emp/', views.add_emp, name="add_emp"),
    path('all_emp/', views.view_all_emp, name="view_all_emp"),
    path('remove_emp/', views.remove_emp, name="remove_emp"),
    path('filter_emp/', views.filter_emp, name="filter_emp"),
]
