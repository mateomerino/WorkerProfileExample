from rest_framework import serializers
from base.models import WorkerProfileExperience, WorkerProfile
from base.serializers import (
    LocationSerializer, ServiceSerializer, TaskSerializer,
    WorkArrangementSerializer, ShiftSerializer, CustomUserSerializer
)


# Serializer para representar un WorkerProfile en JSON.
# Incluye relaciones anidadas: ubicación, servicios, tareas y usuario.
class WorkerProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = WorkerProfile
        depth = 1  # serializa objetos relacionados con un nivel de profundidad
        fields = '__all__'


# Serializer que transforma la experiencia en JSON y valida los datos antes de guardar.
class WorkerProfileExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProfileExperience
        fields = '__all__'

    def validate(self, data):
        """
        Validación de longitud:
        - title ≤ 80 caracteres
        - description ≤ 400 caracteres
        """
        if len(data.get('title', '')) > 80:
            raise serializers.ValidationError("Title must be 80 characters or fewer.")
        if len(data.get('description', '')) > 400:
            raise serializers.ValidationError("Description must be 400 characters or fewer.")
        return data
