from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# QuerySet especializado para WorkerProfile.
# Permite consultas más expresivas sobre la base de datos.
class WorkerProfileQuerySet(models.QuerySet):

    def get_profile_by_user(self, user):
        """
        Retorna el perfil de trabajador asociado a un usuario.
        Devuelve None si no existe.
        """
        return self.filter(user=user).first()

    def get_all(self):
        """
        Retorna todos los perfiles de trabajador,
        ordenados alfabéticamente por el nombre del usuario.
        """
        return self.all().order_by('user__first_name')

    def get_all_visible_profiles(self):
        """
        Retorna todos los perfiles que están configurados como visibles.
        (user.profile_visibility = True)
        """
        return self.filter(user__profile_visibility=True)


# Manager personalizado para WorkerProfile.
# Expone solo los métodos utilizados en las views (get_profile_by_id, update_profile_info).
class WorkerProfileManager(models.Manager):

    def get_queryset(self):
        """
        Sobrescribe el método base para usar WorkerProfileQuerySet.
        Esto habilita los métodos personalizados en las consultas.
        """
        return WorkerProfileQuerySet(self.model, using=self._db)

    def get_profile_by_id(self, profile_id):
        """
        Obtiene un WorkerProfile por su ID.
        Retorna None si no existe.
        """
        try:
            return self.get_queryset().get(id=profile_id)
        except ObjectDoesNotExist:
            return None

    def update_profile_info(self, profile_id, updated_data, location=None):
        """
        Actualiza los campos básicos de un WorkerProfile.
        - profile_id: ID del perfil a actualizar
        - updated_data: diccionario con los datos nuevos
        - location: objeto Location (opcional), se asigna si se pasa

        Retorna el perfil actualizado si tiene éxito,
        o (False, error_message) si ocurre un problema.
        """
        try:
            profile = self.get(id=profile_id)

            # Asignar valores excepto la ubicación, que se maneja aparte
            for key, value in updated_data.items():
                if key != 'location':
                    setattr(profile, key, value)

            # Si se pasa ubicación, asignarla
            if location:
                profile.location = location

            profile.save()
            return profile
        except Exception as e:
            return False, str(e)
