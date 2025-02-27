from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type' : 'password'} ,write_only = True)

    class Meta:

        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def save(self, *args, **kwargs):
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        user = User.objects.filter(email= self.validated_data['email'])

        if password != password2:
            raise serializers.ValidationError({'error' : 'Password and confirm password are not the same'})
        if user.exists():
            raise serializers.ValidationError({'error' : 'This email already exists'})
        
        account = User.objects.create(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account
        