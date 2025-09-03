from django.urls import path
from .views_worker import WorkerProfileExperienceView, WorkerProfileInfoView

# Rutas disponibles para WorkerProfile:
# - Añadir experiencias laborales
# - Actualizar información general (incluyendo ubicación)
urlpatterns = [
    path('<int:profile_id>/experience/add/', WorkerProfileExperienceView.as_view(),
         name='add-worker-profile-experience'),
    path('<int:profile_id>/info/update/', WorkerProfileInfoView.as_view(),
         name='update-worker-profile-info')
]
