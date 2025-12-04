from django.urls import path
from .views import Avaliar_IMC_View, ListarCadastradosIMC_View 

app_name = 'IMC' 

urlpatterns = [
    # Mapeia /imc/avaliar/ para a view de cálculo
    path('avaliar/', Avaliar_IMC_View.as_view(), name='avaliar_imc'),
    
    # Mapeia /imc/listar/ para a view de listagem
    path('listar/', ListarCadastradosIMC_View.as_view(), name='listar_cadastrados_imc'),
]