from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Função auxiliar para classificação do IMC
def classificar_imc(valor_imc):
    """Classifica o valor do IMC de acordo com a tabela da OMS."""
    if valor_imc < 18.5:
        return 'Abaixo do Normal'
    elif valor_imc < 25.0:
        return 'Normal'
    elif valor_imc < 30.0:
        return 'Sobrepeso'
    elif valor_imc < 35.0:
        return 'Obesidade Grau 1'
    elif valor_imc < 40.0:
        return 'Obesidade Grau 2'
    else:
        return 'Obesidade Grau 3'

# CLASSE RENOMEADA para AvaliacaoIMC (sem underscore)
class AvaliacaoIMC(models.Model):
    # CPF como chave primária, valor único e não nulo.
    cpf = models.CharField(
        max_length=11, 
        primary_key=True, 
        unique=True,
        verbose_name='CPF'
    )
    
    nome = models.CharField(max_length=255, verbose_name='Nome Completo')
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    sexo = models.CharField(
        max_length=1, 
        choices=SEXO_CHOICES,
        verbose_name='Sexo'
    )
    
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    escola = models.CharField(max_length=255, verbose_name='Escola')
    
    # Peso (kg) e Altura (m)
    peso = models.FloatField(verbose_name='Peso (kg)')
    altura = models.FloatField(verbose_name='Altura (m)')
    
    # O campo de foto deve armazenar o caminho do arquivo
    foto = models.ImageField(
        upload_to='avaliacoes_fotos/', 
        verbose_name='Foto da Pessoa Avaliada',
        null=True, blank=True # Adicionando null/blank para evitar problemas de validação no formulário se for opcional
    )
    
    # Classificação será armazenada
    classificacao_imc = models.CharField(
        max_length=50, 
        editable=False, 
        verbose_name='Classificação do IMC',
        null=True, blank=True
    )
    
    class Meta:
        verbose_name = 'Avaliação de IMC'
        verbose_name_plural = 'Avaliações de IMC'
        
    def __str__(self):
        return f'{self.nome} ({self.cpf})'

    @property
    def valor_imc(self):
        """Calcula o valor do IMC"""
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0.0

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para calcular e armazenar a classificação do IMC antes de salvar."""
        self.classificacao_imc = classificar_imc(self.valor_imc)
        super().save(*args, **kwargs)

    def clean(self):
        """Validação personalizada para garantir que Altura e Peso sejam positivos."""
        if self.peso <= 0:
            raise ValidationError({'peso': 'O peso deve ser um valor positivo.'})
        if self.altura <= 0:
            raise ValidationError({'altura': 'A altura deve ser um valor positivo.'})
        super().clean()