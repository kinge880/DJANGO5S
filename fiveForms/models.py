from datetime import date
from django.db import models
from sectors.models import sectors
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files import File
from simple_history.models import HistoricalRecords

User = settings.AUTH_USER_MODEL

#tabela com os formulários
class fiveForm(models.Model):
    
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="Formulário")
    description = models.TextField(blank = True, default='', verbose_name="Descrição do formulário")
    userId = models.ForeignKey(User, verbose_name="Usuário que criou o formulário", blank=False, null=False, on_delete=models.PROTECT)
    sectorId = models.ForeignKey(sectors, verbose_name="Setor", blank=False, null=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da criação do formulário")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="última edição")
    start_at = models.DateField(verbose_name="Data e hora de inicio do formulário", blank=False, null=False)
    end_at = models.DateField(verbose_name="Data e hora de fim do formulário", blank=False, null=False)
    history = HistoricalRecords()
    
    @property
    def is_active(self):
        return self.start_at <= date.today() and self.end_at >= date.today()
    
    def __str__(self):
        return self.title

#tabela com as perguntas de cada formulário
class fiveFormAsk(models.Model):
    ASKWEIGHT_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    
    ask = models.TextField(blank=False, null=False, verbose_name="Pergunta")
    askweight = models.IntegerField(choices=ASKWEIGHT_CHOICES, default="3", blank=False, null=False, verbose_name="Peso da pergunta")
    formId = models.ForeignKey(fiveForm, verbose_name="Formulário da pergunta", blank=False, null=False, on_delete=models.PROTECT)
    is_image = models.BooleanField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da pergunta")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="Última edição da pergunta")
    history = HistoricalRecords()
    
    def __str__(self):
        return f'Pergunta: {self.ask} do formulário {self.formId}'

def compress(image):
    im = Image.open(image)
    #verifica se a imagem não ta no formato JPEG e converte caso seja necessário
    if im.mode != "RGB":
        im = im.convert("RGB")
    # cria o objeto BytesIO 
    im_io = BytesIO() 
    # salva imagem como um objeto BytesIO 
    im.save(im_io, 'JPEG', optimize=True, quality=20) 
    # cria o objeto image do django
    new_image = File(im_io, name=image.name)
    return new_image
         
class fiveFormResponseImage(models.Model): 
    image = models.ImageField(upload_to='form/response/%Y%m%d', blank=True, null= True, verbose_name="Imagem de resposta")
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
        return f'Imagem {self.id}'
    
    

#tabela com as respostas de cada pergunta
class fiveFormResponse(models.Model):
    RESPONSEWEIGHT_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )
    
    response = models.TextField(verbose_name="Resposta",  blank=False, null=False,)
    responseweight = models.IntegerField(choices=RESPONSEWEIGHT_CHOICES, default="5", blank=False, null=False, verbose_name="Peso da resposta")
    askId = models.ForeignKey(fiveFormAsk, verbose_name="Pergunta", blank=False, null=False, on_delete=models.PROTECT)
    image = models.ForeignKey(fiveFormResponseImage, verbose_name="imagem", blank=True, null=True, on_delete=models.PROTECT)
    userId = models.ForeignKey(User, verbose_name="usuário que criou a resposta", blank=False, null=False, on_delete=models.PROTECT)
    formId = models.ForeignKey(fiveForm, verbose_name="Formulário da resposta", blank=False, null=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name="Data e hora da da pergunta")
    updated_at = models.DateTimeField(auto_now = True, verbose_name="Última edição da pergunta")
    history = HistoricalRecords()
    
    def __str__(self):
        return f'Resposta da pergunta {self.askId} do formulário {self.formId}'