from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('dashboard/', views.stagiaire_dashboard, name='stagiaire_dashboard'),
    path('postuler/<int:stage_id>/', views.postuler_stage, name='postuler_stage'),
    path('stage/<int:stage_id>/', views.details_stage, name='details_stage'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('delete-application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('stages-disponibles/', views.stages_disponibles, name='stages_disponibles'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('suivi-de-stage/', views.suivi_de_stage, name='suivi_de_stage'),
    path('soumettre-projet/', views.soumettre_projet, name='soumettre_projet'),
    path('upload-files/', views.upload_files, name='upload_files'),
    path('profile/', views.profile, name='profile'),
    path('request-certificate/', views.request_certificate, name='request_certificate'),
    path('download-certificate/<int:request_id>/', views.download_certificate, name='download_certificate'),
]
