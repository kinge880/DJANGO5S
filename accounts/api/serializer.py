from rest_framework import serializers
from fiveForms.models import fiveFormResponse
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from accounts.models import User, office
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import update_last_login

#cria e edita user
class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password','is_superuser', 'is_admin', 'email', 'first_name', 'last_name', 'office','date_joined','last_login' )
        extra_kwargs = {
                'email': {
                    'validators': [
                        UniqueValidator(
                            queryset=User.objects.all(),
                            message = 'Já existe um Usuário registrado com esse email!'
                        )
                    ]
                }
            } 
        
    def create(self, validated_data):
        try:
            return User.objects.create(
                password=make_password(
                    validated_data.pop('password')
                ),
                **validated_data
            )
        except ValidationError as ex:
            raise serializers.ValidationError("O formulário não é valido!")

#cria e edita user
class userGetSerializers(serializers.ModelSerializer):
    office = serializers.StringRelatedField()
    fives_cont = fiveFormResponse.objects.all().values_list('id', flat=True).distinct()    
    
    class Meta:
        model = User
        fields = ('id','is_superuser', 'is_admin', 'image','email', 'first_name', 'last_name', 'office','date_joined','last_login' )
        extra_kwargs = {
                    'email': {
                        'validators': [
                            UniqueValidator(
                                queryset = User.objects.all(),
                                message = 'Já existe um Usuário registrado com esse email!'
                            )
                        ]
                    }
                }
   
#troca a senha com base na senha antiga e uma senha nova com confirmação dupla
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Sua senha atual está incorreta, por favor tente novamente')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                ("As senhas não são iguais")
            )
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

#Cria e edita a instancia de cargos
class officeSerializer(serializers.ModelSerializer):
    class Meta:
        model = office 
        fields = ('id','name', 'description', 'created_at', 'updated_at')
        xtra_kwargs = {
                'name': {
                    'validators': [
                        UniqueValidator(
                            queryset=office.objects.all(),
                            message = 'Já existe um cargo registrado com esse nome!'
                        )
                    ]
                }
            }      
    
    def create(self, validated_data):
        return office.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = userSerializers(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
class RefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
       
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        
        return data