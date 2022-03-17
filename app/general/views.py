from core.custom_responses import CustomResponses
from core.docs.sample_responses.sample_district_response import SampleDistrictResponses
from core.docs.sample_responses.sample_state_response import SampleStateResponses
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView

from general import models

from . import serializers


class StateView(GenericAPIView):
    """To manage state list API"""

    serializer_class = serializers.StateSerializer

    @swagger_auto_schema(
        responses=SampleStateResponses().get_all_states_response(),
        query_serializer=serializers.StateSerializer,
    )
    def get(self, _):
        state_data = models.State.objects.all()
        serialized_data = serializers.StateSerializer(state_data, many=True)
        states = list(serialized_data.data)
        return CustomResponses.get_states_response(states)


class StateDetailView(GenericAPIView):
    """To manage state detail API"""

    serializer_class = serializers.StateSerializer

    @swagger_auto_schema(
        responses=SampleStateResponses().get_all_states_response(),
        query_serializer=serializers.StateSerializer,
    )
    def get(self, _, pk):
        try:
            state = models.State.objects.get(pk=pk)
            serialized_state = serializers.StateSerializer(state)
            return CustomResponses.get_state_response(serialized_state.data)
        except:
            return CustomResponses.single_error_response(
                "Requested State could not be found"
            )


class DistrictView(GenericAPIView):
    """To manage district API"""

    serializer_class = serializers.DistrictSerializer

    @swagger_auto_schema(
        responses=SampleDistrictResponses().get_all_districts_response(),
        query_serializer=serializers.DistrictSerializer,
    )
    def get(self, request):
        state_id = request.query_params.get("state_id")
        district_data = self.get_districts(state_id)
        serialized_data = serializers.DistrictSerializer(district_data, many=True)
        districts = list(serialized_data.data)
        return CustomResponses.get_districts_response(districts)

    def get_districts(self, state_id):
        if not state_id:
            district_data = models.District.objects.all()
        else:
            district_data = models.District.objects.filter(state_id=state_id)
        return district_data


class DistrictDetailView(GenericAPIView):
    """To manage district details API"""

    serializer_class = serializers.DistrictSerializer

    @swagger_auto_schema(
        responses=SampleDistrictResponses().get_district_detail_response(),
        query_serializer=serializers.DistrictSerializer,
    )
    def get(self, _, pk):
        try:
            district = models.District.objects.get(pk=pk)
            serialized_district = serializers.DistrictSerializer(district)
            return CustomResponses.get_district_response(serialized_district.data)
        except:
            return CustomResponses.single_error_response(
                "Requested District could not be found"
            )
