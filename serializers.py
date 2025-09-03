from rest_framework import serializers
from base.models import WorkerProfileExperience
from base.models import WorkerProfile
from base.serializers import (
    LocationSerializer, ServiceSerializer, TaskSerializer,
    WorkArrangementSerializer, ShiftSerializer, CustomUserSerializer
)


# Serializer que transforma un WorkerProfile en JSON
# Incluye relaciones anidadas: ubicación, servicios, tareas, etc.
class WorkerProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    work_arrangements = WorkArrangementSerializer(many=True, read_only=True)
    work_shifts = ShiftSerializer(many=True, read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = WorkerProfile
        depth = 1  # profundidad de relaciones para serializar objetos anidados
        fields = '__all__'

        
# Serializer que transforma la experiencia en JSON y valida la data
class WorkerProfileExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProfileExperience
        fields = '__all__'

    # Validación de longitudes antes de guardar en la DB
    def validate(self, data):
        if len(data.get('title', '')) > 80:
            raise serializers.ValidationError("Title must be 80 characters or fewer.")
        if len(data.get('description', '')) > 400:
            raise serializers.ValidationError("Description must be 400 characters or fewer.")
        return data



