
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Api.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializers,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from Api .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Genrate Token manualy

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# import io
# from rest_framework.parsers import JSONParser
# from .models import PersonalDetails
# from .serializers import ResumeSerializers  # Ensure this does not import PersonalDetails directly
# from rest_framework.renderers import JSONRenderer
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt


 
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_404_BAD_REQUEST)
    



class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Authenticate using email and password
            user = authenticate(request, username=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'errors': {'non_field_errors': ['Email or Password is not valid']}},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserProfileView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
         serializer= UserProfileSerializers(request.user)
        #  if serializer.is_valid():
         return Response(serializer.data, status=status.HTTP_200_OK) 
          


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Updated Success...'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
# from rest_framework import status

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Reset Password Link sent to your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid,token , format=None):
        serilizer = UserPasswordResetSerializer(data=request.data,context={'uid':uid, 'token':token})
        if serilizer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Success'}, status=status.HTTP_200_OK)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)







# # Disable CSRF for simplicity (only for development/testing purposes)
# @csrf_exempt
# def Personal_api(request):
#     # Handle GET requests
#     if request.method == "GET":
#         # Parse incoming JSON data
#         json_data = request.body
#         if not json_data:
#             return JsonResponse({'error': 'No data provided'}, status=400)
        
#         stream = io.BytesIO(json_data)
#         python_data = JSONParser().parse(stream)

#         # Get 'id' from parsed data (optional)
#         student_id = python_data.get('id', None)

#         # If an ID is provided, return details of the specific student
#         if student_id is not None:
#             try:
#                 student = PersonalDetails.objects.get(id=student_id)
#                 serializer = PersonalDetails(student)
#                 json_data = JSONRenderer().render(serializer.data)
#                 return HttpResponse(json_data, content_type='application/json')
#             except PersonalDetails.DoesNotExist:
#                 return JsonResponse({'error': 'Student not found'}, status=404)

#         # If no ID is provided, return all students
#         students = PersonalDetails.objects.all()
#         serializer = ResumeSerializers(students, many=True)
#         json_data = JSONRenderer().render(serializer.data)
#         return HttpResponse(json_data, content_type='application/json')

#     # Handle POST requests
#     elif request.method == 'POST':
#         # Check if the request body contains data
#         if not request.body:
#             return JsonResponse({'error': 'No data provided'}, status=400)

#         # Parse incoming JSON data
#         stream = io.BytesIO(request.body)
#         python_data = JSONParser().parse(stream)
#         print('python data',python_data)

#         # Deserialize data and validate
#         serializer = ResumeSerializers(data=python_data)
#         if serializer.is_valid():
#             serializer.save()  # Save the student data
#             res = {'msg': 'Data inserted successfully'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
        
#         # If invalid, return errors
#         json_data = JSONRenderer().render(serializer.errors)
#         return HttpResponse(json_data, content_type='application/json', status=400)
    