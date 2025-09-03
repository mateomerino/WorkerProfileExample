from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import WorkerProfileExperience, WorkerProfile, Location, Municipality, Province
from base.serializers import WorkerProfileExperienceSerializer, WorkerProfileSerializer


# View para manejar la información general de un WorkerProfile
class WorkerProfileInfoView(APIView):
    def put(self, request, profile_id, format=None):
        """
        Actualiza los datos de un WorkerProfile.
        Si se incluyen datos de ubicación (neighborhood, municipality, province),
        crea o actualiza el objeto Location asociado.
        """
        updated_data = request.data
        wp = WorkerProfile.objects.get_profile_by_id(profile_id)

        neighborhood = updated_data.get('neighborhood')
        municipality_id = updated_data.get('municipality')
        province_id = updated_data.get('province')

        # Crear o actualizar Location si hay datos
        if neighborhood is not None or municipality_id is not None or province_id is not None:
            municipality = Municipality.objects.get_by_id(municipality_id)
            province = Province.objects.get_by_id(province_id)

            if wp.location_id:
                loc = Location.objects.get_by_id(wp.location_id)
                Location.objects.update_location(loc, neighborhood, province, municipality)
            else:
                loc = Location.objects.create_location(neighborhood, province, municipality)
        else:
            loc = None

        updated_profile = WorkerProfile.objects.update_profile_info(profile_id, updated_data, loc)

        return Response(
            WorkerProfileSerializer(updated_profile).data,
            status=status.HTTP_200_OK
        )


# View para manejar experiencias laborales de un WorkerProfile
class WorkerProfileExperienceView(APIView):
    def post(self, request, profile_id):
        """
        Crea una nueva experiencia laboral asociada al WorkerProfile.
        Valida los datos con WorkerProfileExperienceSerializer
        y persiste en la base de datos si son correctos.
        """
        data = request.data.copy()
        data['worker'] = profile_id

        serializer = WorkerProfileExperienceSerializer(data=data)

        if serializer.is_valid():
            exp = WorkerProfileExperience.objects.create_experience(**serializer.validated_data)
            return Response(
                WorkerProfileExperienceSerializer(exp).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
