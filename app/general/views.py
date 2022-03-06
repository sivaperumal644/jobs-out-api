from core.custom_responses import CustomResponses
from core.docs.sample_responses.sample_state_response import SampleStateResponses
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView

from general import models

from . import serializers


class StateView(GenericAPIView):
    """To manage state api"""

    serializer_class = serializers.StateSerializer

    @swagger_auto_schema(
        responses=SampleStateResponses().get_all_states_response(),
        query_serializer=serializers.StateSerializer,
    )
    def get(self, _):
        stateData = models.State.objects.all()
        serialized_data = serializers.StateSerializer(stateData, many=True)
        states = list(serialized_data.data)
        return CustomResponses.get_states_response(states)
