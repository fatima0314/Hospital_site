from rest_framework import viewsets, generics, permissions, status
from rest_framework.exceptions import ValidationError
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DoctorPagination
from .permissions import CheckAppointment, CheckMedicalRecord, CheckAdmin, CheckAll
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
       try:
           serializer = self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           user = serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       except serializers.ValidationError:
           return Response({'detail':'Туура эмес маалымат'}, status.HTTP_400_BAD_REQUEST)
       except NameError as e:
           return Response({'detail':f'{e}, Код туура эмес'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(TokenObtainPairView):
    serializer_class =LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status = status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs ):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'detail':'Ключ туура эмес'}, status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)


class ProfileCreateApiView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [CheckAll]


class SpecialityApiView(generics.ListCreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    permission_classes = [CheckAdmin]


class DoctorListApiView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['specialty', 'price', 'working_days']
    ordering_fields = ['price']
    pagination_class = DoctorPagination


class DoctorDetailApiView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer


class DoctorCreateApiView(generics.CreateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [CheckAll]


class PatientListApiView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer


class PatientDetailApiView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    searching_fields = ['name']
    permission_classes = [CheckAdmin]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [CheckAdmin]


class AppointmentCreateApiView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes =  [CheckAll, CheckAppointment]


class MedicalRecordApiView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [CheckAdmin, CheckMedicalRecord]


class PrescriptionsViewSet(viewsets.ModelViewSet):
    queryset = Prescriptions.objects.all()
    serializer_class = PrescriptionsSerializer
    permission_classes = [CheckAdmin]


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [CheckAdmin]


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [CheckAdmin]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [CheckAppointment]