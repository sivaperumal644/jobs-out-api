from core.custom_responses import CustomResponses
from core.docs.sample_responses.sample_state_response import SampleStateResponses
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView

from general import models

from . import serializers


class StateView(GenericAPIView):
    """To manage state API"""

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


class DistrictView(GenericAPIView):
    """To manage district API"""

    serializer_class = serializers.DistrictSerializer

    def get(self, _):
        district_data = models.District.objects.all()
        serialized_data = serializers.DistrictSerializer(district_data, many=True)
        districts = list(serialized_data.data)
        return CustomResponses.get_districts_response(districts)
