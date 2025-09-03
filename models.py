from django.db import models
from base.models import UserProfile, Language, Service, Task, Location

# Perfil del trabajador:
# Representa la "tarjeta" que un trabajador publica en la plataforma.
# Incluye datos personales, su presentación, servicios ofrecidos, tareas y ubicación.
class WorkerProfile(UserProfile):

    # Opciones de género para los perfiles
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
    ]

    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)

    services = models.ManyToManyField(Service)

    tasks = models.ManyToManyField(Task)

    #: Fecha de nacimiento del trabajador
    date_of_birth = models.DateField(null=True, blank=True)

    #: Género (Masculino / Femenino), opcional
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)



    class Meta:
        verbose_name = "Worker Profile"
        verbose_name_plural = "Worker Profiles"

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save estándar de Django.
        Actualmente no agrega lógica extra, 
        pero puede extenderse en el futuro (ej: validaciones personalizadas).
        """
        super(WorkerProfile, self).save(*args, **kwargs)


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
