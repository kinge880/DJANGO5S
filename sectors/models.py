from django.db import models
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files import File
from simple_history.models import HistoricalRecords

User = settings.AUTH_USER_MODEL
def compress(image):
    im = Image.open(image)
    #verifica se a imagem não ta no formato JPEG e converte caso seja necessário
    if im.mode != "RGB":
        im = im.convert("RGB")
    # cria o objeto BytesIO 
    im_io = BytesIO() 
    # salva imagem como um objeto BytesIO 
    im.save(im_io, 'JPEG', optimize=True, quality=40) 
    # cria o objeto image do django
    new_image = File(im_io, name=image.name)
    return new_image

class sectorsImage(models.Model): 
    image = models.ImageField(upload_to='sectors', blank=False, null= False, verbose_name="Imagem do setor")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora do envio da imagem")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="Última edição da imagem")
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        # chama a função de comp ressão
        new_image = compress(self.image)
        # seta self.image com a nova imagem
        self.image = new_image
        # salva
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'http://127.0.0.1:8000/media/{self.image}'
    
class userSectors(models.Model):
    STATUS_CHOICES = (
        ("P", "Pendente"),
        ("N", "Negado"),
        ("A", "Aceito")
    )
    
    SUPERVISOR_CHOICES = (
        ("N", "Não"),
        ("S", "Sim"),
    )
    
    userId = models.ForeignKey(User, verbose_name="Usuário", blank=False, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P", blank=False, null=False)
    description = models.TextField(blank = True, default='', verbose_name="Motivo da liberação")
    supervisor = models.CharField(max_length=1, choices=SUPERVISOR_CHOICES, default="N", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da liberação do setor")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    history = HistoricalRecords()
    
    class Meta:
        verbose_name_plural = "Usuários/Setores"
        verbose_name = 'Usuário/Setor' 
    
    def __str__(self):
        return f'Usuário: {self.userId} | Setor: {self.sectorId}'


class branch(models.Model):
    
    address = models.TextField(max_length=255,  blank=False, null=False)
    number = models.IntegerField(blank = False, null = False, unique=True)
    is_active = models.BooleanField(default=True, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da liberação do setor")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    history = HistoricalRecords()
    
    class Meta:
        verbose_name_plural = "Filiais"
        verbose_name = 'Filial' 
    
    def __str__(self):
        
        return f'Filial: {self.number}'
    
class sectorsGroup(models.Model):

    name = models.CharField(max_length = 255, null=False, blank=False, verbose_name="Nome do setor")
    image = models.ForeignKey(sectorsImage, blank=False, null=False, verbose_name="Imagem", on_delete=models.PROTECT)
    branchName = models.ForeignKey(branch, blank=False, null=False, verbose_name="filial", on_delete=models.PROTECT)
    description = models.TextField(blank = True, default='', verbose_name="Descrição do setor")
    is_active = models.BooleanField(default = True, verbose_name="O setor ta ativo?")
    desactive_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de desativação do setor")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data de criação do setor")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="Última edição das informações do setor")
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Setores"
        verbose_name = 'Setor' 
        ordering = ['created_at']
    def __str__(self):
        return self.name
    
class sectors(models.Model):

    name = models.CharField(max_length = 255, null=False, blank=False, verbose_name="Nome do setor")
    image = models.ForeignKey(sectorsImage, blank=False, null=False, verbose_name="Imagem", on_delete=models.PROTECT)
    branchName = models.ForeignKey(branch, blank=False, null=False, verbose_name="filial", on_delete=models.PROTECT)
    sectorGroup = models.ForeignKey(sectorsGroup, blank=False, null=False, verbose_name="Grupo de setores", on_delete=models.PROTECT)
    description = models.TextField(blank = True, default='', verbose_name="Descrição do setor")
    is_active = models.BooleanField(default = True, verbose_name="O setor ta ativo?")
    desactive_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de desativação do setor")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data de criação do setor")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="Última edição das informações do setor")
    history = HistoricalRecords()
    
    class Meta:
        verbose_name_plural = "SubSetores"
        verbose_name = 'SubSetor' 
        ordering = ['created_at']
    def __str__(self):
        return self.name
    