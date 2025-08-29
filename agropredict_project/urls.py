from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', core_views.dashboard, name='dashboard'),
    path('prediccion/', core_views.prediccion_form, name='prediccion_form'),
    path('prediccion/<int:pk>/', core_views.prediccion_resultado, name='prediccion_resultado'),
    path("api/comunas/<slug:region_slug_value>/", core_views.comunas_api, name="api_comunas"),
]
