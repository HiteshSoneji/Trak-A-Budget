from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/home/', views.home, name='home'),
    path('accounts/login_corp/', views.org_login_view, name='login_corp'),
    path('accounts/register_corp/', views.org_register_view, name = 'org_register'),
    path('accounts/register_ind/', views.ind_register_view, name='ind_register'),
    path('accounts/login_ind/', views.ind_login_view, name = 'ind_login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/home_graph/', views.graph_view, name='graph'),
    path('accounts/home_expenses/', views.expense_view, name='expenses'),
    path('accounts/org_register/', views.org_register_view, name = 'org_register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.splash, name='splash'),
]