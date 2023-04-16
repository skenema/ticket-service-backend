from django.urls import path
from . import views

urlpatterns = [
    path('tickets', views.get_ticket),
    path('validate-ticket', views.validate_ticket),
    path('create-ticket', views.create_ticket),
    path('delete-ticket', views.delete_ticket)
]
