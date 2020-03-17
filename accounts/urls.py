from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/home/', views.home, name='home'),
    path('accounts/home/<int:int_object>', views.home1, name='home1'),
    path('accounts/home_corp/', views.home_corp, name='home_corp'),
    path('accounts/home_corp/<int:int_object1>/<int:int_object2>', views.home_corp1, name='home_corp1'),
    path('accounts/login_corp/', views.org_login_view, name='login_corp'),
    path('accounts/register_corp/', views.org_register_view, name = 'org_register'),
    path('accounts/register_ind/', views.ind_register_view, name='ind_register'),
    path('accounts/login_ind/', views.ind_login_view, name = 'ind_login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/home_graph/', views.graph_view, name='graph'),
    path('accounts/home_graph_corp/', views.graph_view_corp, name='graph_corp'),
    path('accounts/home_expenses/', views.expense_view, name='expenses'),
    path('accounts/org_register/', views.org_register_view, name = 'org_register'),
    path('accounts/indiv_pdf/', views.indiv_pdf_view, name='ind_pdf'),
    path('accounts/corp_pdf/', views.corp_pdf_view, name='corp_pdf'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.splash, name='splash'),
]