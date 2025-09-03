from django.db import models

# Perfil del trabajador
class WorkerProfile(UserProfile):

    GENDER_CHOICES = [
        ('male', 'Masculino'), 
        ('female', 'Femenino'), 
    ]

    introduction = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    languages = models.ManyToManyField(Language, through='WorkerLanguage')
    services = models.ManyToManyField(Service)
    tasks = models.ManyToManyField(Task)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Worker Profile"
        verbose_name_plural = "Worker Profiles"
    
    def save(self, *args, **kwargs):
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
