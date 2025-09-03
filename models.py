from django.db import models

# Perfil del trabajador (se define completo en tu backend real)
class WorkerProfile(models.Model):
    # … campos de WorkerProfile (introducción, precio/hora, etc.)
    pass

# Experiencia laboral asociada a un WorkerProfile
class WorkerProfileExperience(models.Model):
    # Título de la experiencia, ej. "Niñera part-time"
    title = models.CharField(max_length=80)

    # Breve descripción de tareas y responsabilidades
    description = models.TextField(max_length=400)

    # Booleano que indica si el trabajador sigue en esa experiencia actualmente
    currently_working = models.BooleanField()

    # Relación: cada experiencia pertenece a un WorkerProfile
    worker = models.ForeignKey(
        WorkerProfile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
