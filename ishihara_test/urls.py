from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('test/<str:test_type>/', views.test_view, name='test'),
    path('submit/', views.submit_test, name='submit_test'),
    path('share/<str:token>/', views.share_view, name='share'),
    path('results/<str:uuid>/', views.show_results, name='results'),
    path('contact/', views.contact_view, name='contact'),
]
