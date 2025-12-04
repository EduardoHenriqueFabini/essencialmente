from django import forms
from .models import AvaliacaoIMC

class AvaliarIMCForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoIMC
        # CORREÇÃO: O nome do campo no model é 'classificacao_imc', não 'classificacao'
        exclude = ('classificacao_imc', 'classificacao', 'data_avaliacao',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Itera sobre todos os campos para adicionar a classe de estilo
        for name, field in self.fields.items():
            # Aplica a classe padrão
            if field.widget.__class__.__name__ not in ['CheckboxInput', 'ClearableFileInput']:
                field.widget.attrs.update({'class': 'form-control'}) # Bootstrap usa 'form-control', não 'form-field'

            # Ajuste específico para o campo de data
            if name == 'data_nascimento':
                self.fields[name].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            
            # Placeholders
            if name in ['cpf', 'nome', 'peso', 'altura', 'escola']:
                placeholders = {
                    'cpf': '000.111.222-33',
                    'nome': 'Nome completo',
                    'peso': 'Ex: 55.5',
                    'altura': 'Ex: 1.65',
                    'escola': 'Nome da Escola',
                }
                field.widget.attrs['placeholder'] = placeholders.get(name, '')