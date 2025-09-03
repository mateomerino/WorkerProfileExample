from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import WorkerProfileExperience
from base.serializers import WorkerProfileExperienceSerializer
from base.models import WorkerProfile, Location, Municipality, Province
from base.serializers import WorkerProfileSerializer



# View que maneja la información general del WorkerProfile
class WorkerProfileInfoView(APIView):

    # Método PUT: actualizar datos del perfil y su ubicación asociada
    def put(self, request, profile_id, format=None):
        # Data entrante del frontend
        updated_data = request.data

        # Buscar el perfil por id
        wp = WorkerProfile.objects.get_profile_by_id(profile_id)

        # Extraer posibles campos de ubicación del request
        neighborhood = updated_data.get('neighborhood')
        municipality_id = updated_data.get('municipality')
        province_id = updated_data.get('province')

        # Si hay datos de ubicación, crear o actualizar Location
        if neighborhood is not None or municipality_id is not None or province_id is not None:
            municipality = Municipality.objects.get_by_id(municipality_id)
            province = Province.objects.get_by_id(province_id)

            # Si ya existe Location → actualizar, si no → crear
            if wp.location_id:
                loc = Location.objects.get_by_id(wp.location_id)
                Location.objects.update_location(loc, neighborhood, province, municipality)
            else:
                loc = Location.objects.create_location(neighborhood, province, municipality)
        else:
            loc = None

        # Actualizar el perfil con la nueva información y la ubicación
        updated_profile = WorkerProfile.objects.update_profile_info(profile_id, updated_data, loc)

        # Responder con el perfil actualizado en formato JSON
        return Response(
            WorkerProfileSerializer(updated_profile).data,
            status=status.HTTP_200_OK
        )
    
# View que maneja las operaciones relacionadas a experiencias de un WorkerProfile
class WorkerProfileExperienceView(APIView):

    # Método POST: crear una nueva experiencia laboral
    def post(self, request, profile_id):
        # Incorporar el id del perfil al payload
        data = request.data.copy()
        data['worker'] = profile_id

        # Serializar la data entrante
        serializer = WorkerProfileExperienceSerializer(data=data)

        # Validar y crear experiencia en la base de datos
        if serializer.is_valid():
            exp = WorkerProfileExperience.objects.create_experience(**serializer.validated_data)
            return Response(
                WorkerProfileExperienceSerializer(exp).data,
                status=status.HTTP_201_CREATED
            )

        # Si hay errores de validación, retornarlos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



