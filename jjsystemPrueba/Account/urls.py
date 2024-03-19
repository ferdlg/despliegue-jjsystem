from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.userLogin, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
    # Ruta para el formulario de solicitud de restablecimiento de contraseña
    path('reestablecer_password_form/', views.password_reset_request, name='password_reset_request_form'),
    # Ruta para la vista de solicitud de restablecimiento de contraseña
    path('reestablecer_password/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    # Ruta para la vista de confirmación de restablecimiento de contraseña
    path('reestablecer_password_enlace/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_enlace'),
    # Ruta para el formulario de confirmación de restablecimiento de contraseña
    
]