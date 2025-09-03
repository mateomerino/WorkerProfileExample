from django.urls import path
from .views_worker import WorkerProfileExperienceView
from .views_worker import WorkerProfileInfoView

# Ruta para crear una nueva experiencia dentro de un WorkerProfile y para actualizar información general de un WorkerProfile
urlpatterns = [
    path('<int:profile_id>/experience/add/', WorkerProfileExperienceView.as_view(),
         name='add-worker-profile-experience'),
    path('<int:profile_id>/info/update/', WorkerProfileInfoView.as_view(),
         name='update-worker-profile-info')
]
