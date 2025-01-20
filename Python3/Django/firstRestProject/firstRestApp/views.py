from django.shortcuts import render
from django.http import JsonResponse
from firstRestApp.models import Employee, Student
from firstRestApp.serializers import StudentSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# Create your views here.
def employeeView(request):
    data = Employee.objects.all()
    response = {'employees': list(data.values('name', 'salary'))}

    return JsonResponse(response)



class StudentPagination(PageNumberPagination):
    page_size=2


#Model Viewset
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = LimitOffsetPagination
    # filter_backends = [filters.SearchFilter]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'score']
    ordering = ['score']
    filterset_fields = ['id', 'name']
    search_fields = ['^id', '^name']
    authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated, DjangoModelPermissions]
    permission_classes=[IsAuthenticated]


#Generics Example
'''
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
'''

# Mixin Example
'''
class StudentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
class StudentView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

'''     




#-- Sample runction based REST API

# @api_view(['GET', 'POST'])
# def student_list(request):
#     if request.method == "GET":
#         students = Student.objects.all()
#         studentSerializer = StudentSerializer(students, many=True)
#         return Response(studentSerializer.data)
#     elif request.method == "POST":
#         studentSerializer = StudentSerializer(data=request.data)
#         if studentSerializer.is_valid():
#             studentSerializer.save()
#             return Response(studentSerializer.data, status=status.HTTP_201_CREATED)
#         return Response(studentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def student_detail(request, pk):
#     try:
#         student = Student.objects.get(pk=pk)
#     except Student.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method =="GET":
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#          serializer = StudentSerializer(student, data=request.data)
#          if serializer.is_valid():
#              serializer.save()
#              return Response(serializer.data)
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         student.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


'''

class StudentList(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentView(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''