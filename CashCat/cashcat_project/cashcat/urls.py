from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('logout/', views.logout_view, name='logout'),
]