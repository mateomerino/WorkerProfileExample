from django.db import models
from base.models import UserProfile, Language, Service, Task, Location


# Perfil del trabajador:
# Representa la tarjeta que un trabajador publica en la plataforma.
# Incluye información básica como ubicación, servicios, tareas, fecha de nacimiento y género.
class WorkerProfile(UserProfile):
    # Opciones de género disponibles
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
    ]

    #: Relación 1:1 con la ubicación (barrio, municipio, provincia)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)

    #: Servicios que el trabajador ofrece (niñera, limpieza, cocina, etc.)
    services = models.ManyToManyField(Service)

    #: Tareas específicas asociadas al servicio (planchado, cuidado de niños, limpieza, etc.)
    tasks = models.ManyToManyField(Task)

    #: Fecha de nacimiento del trabajador
    date_of_birth = models.DateField(null=True, blank=True)

    #: Género del trabajador
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = "Worker Profile"
        verbose_name_plural = "Worker Profiles"

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save estándar de Django.
        Actualmente no agrega lógica extra,
        pero está preparado para extenderse (ej: validaciones personalizadas).
        """
        super(WorkerProfile, self).save(*args, **kwargs)


# Experiencia laboral asociada a un WorkerProfile
class WorkerProfileExperience(models.Model):
    #: Título de la experiencia, ej. "Niñera part-time"
    title = models.CharField(max_length=80)

    #: Breve descripción de tareas y responsabilidades
    description = models.TextField(max_length=400)

    #: Indica si el trabajador sigue desempeñando esa experiencia
    currently_working = models.BooleanField()

    #: Relación: cada experiencia pertenece a un WorkerProfile
    worker = models.ForeignKey(
        WorkerProfile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
