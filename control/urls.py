from django.urls import path
from control import views

urlpatterns = [

    path('app_lobby/', views.app_lobby, name='app_lobby'),

    # LOGIN
    # path('login/',views.iniciar_sesion_form, name="iniciar_sesion_form"),
]
