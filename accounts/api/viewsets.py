from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from accounts.api import serializer
from accounts.models import User, office
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models.deletion import ProtectedError
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from email.mime.text import MIMEText

#Rota de usuários
class userManageViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.userGetSerializers
    http_method_names = ['get', 'put', 'patch']    
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email']
    search_fields = ['email', 'first_name','last_name']
    ordering_fields = ['email', 'first_name', 'office','date_joined','last_login']

class ProfileAPI(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.userGetSerializers
    http_method_names = ['get','put', 'patch']
    queryset = User.objects.all()
    
    def get_queryset(self):                                           
        return super().get_queryset().filter(id=self.request.user.id)

class ProfileAPIEdit(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.userSerializers
    http_method_names = ['get','put', 'patch']
    queryset = User.objects.all()
    
    def get_queryset(self):                                           
        return super().get_queryset().filter(id=self.request.user.id)

#rota de registro de usuário
class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = serializer.userSerializers
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    

#rota para atualizar o token de acesso
# class RefreshViewSet(viewsets.ViewSet, RefreshToken):
class RefreshViewSet(ModelViewSet, RefreshToken):
    serializer_class = serializer.RefreshSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

#Rota de login no sistema
class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = serializer.LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            User.objects.filter(email=request.data['email']).update(last_login=timezone.now())
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
 
 #rota ainda em construção para trocar a senha   
class ChangePasswordView(viewsets.ModelViewSet):
        serializer_class = serializer.ChangePasswordSerializer
        http_method_names = ['patch']
        permission_classes = (IsAuthenticated,)
        
        def update(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(status=status.HTTP_200_OK)

#rota que permite alterar e inserir cargos
class officeViewset(viewsets.ModelViewSet):
    serializer_class = serializer.officeSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post', 'get','put','delete']    
    queryset = office.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name', 'description']
    
    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError as e:
            return Response('Existem um ou mais usuários anexados a esse cargo, troque o cargo desses usuários antes de tentar novamente!', status=status.HTTP_403_FORBIDDEN)
        
        return Response('sucesso', status=status.HTTP_200_OK)

#rota para obter cargos
class officeGetViewset(viewsets.ModelViewSet):
    serializer_class = serializer.officeSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']
    queryset = office.objects.all()
    

#rota para troca de senha pelo email
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = f"Olá, Recebemos uma solicitação para redefinir a senha da sua conta para este endereço de e-mail. \nPara iniciar o processo de redefinição de senha para sua conta, copie o código abaixo:\n {reset_password_token.key} \nE acesse o link: http://localhost:3000/resetarsenha/confirmar \n\nEste código só pode ser usado uma vez. Se você precisar redefinir sua senha novamente, visite http://localhost:3000/resetarsenha e solicite outra redefinição. Se você não fez essa solicitação, simplesmente ignore este e-mail. \nSinceramente, equipe de TI"

    send_mail(
        # title:
        "Recuperação de senha do {title}".format(title="Mercale 5S"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )