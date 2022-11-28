from django.urls import path
from . import views

urlpatterns = [
    path('',views.paypalorderidgen),
    path('create_purchase/',views.create_purchase),
]