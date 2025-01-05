from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DoctorPagination
from .permissions import CheckAppointment, CheckMedicalRecord
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data,  status=status.HTTP_201_CREATED)


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
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)



class ProfileCreateApiView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permissions = [permissions.IsAdminUser]



class SpecialityApiView(generics.ListCreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    permissions = [permissions.IsAdminUser]


class DoctorListApiView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['specialty', 'price', 'working_days']
    ordering_fields = ['price']
    pagination_class = [DoctorPagination]


class DoctorDetailApiView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer


class DoctorCreateApiView(generics.CreateAPIView):
    serializer_class = DoctorCreateSerializer
    permissions = [permissions.IsAdminUser]



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
    permissions = [permissions.IsAdminUser]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]



class AppointmentCreateApiView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes =  [permissions.IsAdminUser, CheckAppointment]



class MedicalRecordApiView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAdminUser, CheckMedicalRecord]



class PrescriptionsViewSet(viewsets.ModelViewSet):
    queryset = Prescriptions.objects.all()
    serializer_class = PrescriptionsSerializer
    permissions = [permissions.IsAdminUser]



class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permissions = [permissions.IsAdminUser]



class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permissions = [permissions.IsAdminUser]



class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [CheckAppointment]