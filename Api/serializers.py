from rest_framework import serializers
from .models import PersonalDetails
from Api.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2  =serializers.CharField(style={'input_type':'password'}
                                      ,write_only=True)
    class Meta:
        model =  User
        fields = ['email','name','password','password2','tc']
        extra_kwargs ={
            'password' :{'write_only':True}

        }
        # Validate  password and Conform Password  while  Registration

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'password2':'Password does not match'})
        return attrs
        
    def create(self, validated_data): 
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {
            'password':{'write_only':True}
            }
        

class UserProfileSerializers(serializers.ModelSerializer):
     class Meta:
         model = User
         fields =['id','email','name']
        


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=3,style={'input_type':'password'}, write_only=True)

    password2 = serializers.CharField(max_length=255, min_length=3,style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError({'password2':'Password does not match'})
        
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')




class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


# class UserPasswordResetSerializers(serializers.Serializer):
#         password = serializers.CharField(max_length=255, min_length=3,style={'input_type':'password'}, write_only=True)

#         password2 = serializers.CharField(max_length=255, min_length=3,style={'input_type':'password'}, write_only=True)
#         class Meta:
#             fields = ['password','password2']
#         def validate(self, attrs):
#             try:
#                 password = attrs.get('password')
#                 password2 = attrs.get('password2')
#                 uid = self.context.get('uid')
#                 token = self.context.get('token')
#                 if password != password2:
#                     raise serializers.ValidationError({'password2':'Password does not match'})
#                 id  = smart_str(urlsafe_base64_decode(uid))
#                 user = User.objects.get(id=id)
#                 if not PasswordResetTokenGenerator().check_token(user, token):
#                     raise serializers.ValidationError({'password2':'Invalid token'})
                
#                 user.set_password(password)
#                 user.save()
#                 return attrs
#             except DjangoUnicodeDecodeError as identifier:
#                 PasswordResetTokenGenerator().check_token(user, token)
#                 raise serializers.ValidationError({'password2':'Token is invalid or has expired'})

 

# class ResumeSerializers(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=254)
#     mobile = serializers.CharField(max_length=15)
#     address = serializers.CharField()
#     linkedin_url = serializers.URLField(max_length=200, required=False, allow_blank=True)  # Allow blank
#     github_link = serializers.URLField(max_length=200, required=False, allow_blank=True)  # Allow blank

#     def create(self, validated_data):
#         return PersonalDetails.objects.create(**validated_data)

#     def validate_email(self, value):
#         if PersonalDetails.objects.filter(email=value).exists():
#             raise serializers.ValidationError("This email is already in use.")
#         return value
