from rest_framework.generics import ListCreateAPIView
from .serializers import BookingSerializer
from .models import Booking


class BookingAPIView(ListCreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
