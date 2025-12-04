from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from IMC.views import Avaliar_IMC_View
from IMC.views import index 

# IMPORTAÇÃO CRÍTICA: Importa a view 'index' para ser a homepage
from IMC.views import index 

urlpatterns = [
    # ROTA DA HOMEPAGE: Mapeia o caminho vazio ('') para a view index. ISSO CORRIGE O 404.
    path('', index, name='home'), 
    
    # Rota padrão para o painel de administração
    path('admin/', admin.site.urls),
    
    # Rota que inclui todas as URLs do seu aplicativo IMC
    path('imc/', include('IMC.urls')), 
]

# Configuração para servir arquivos de mídia (Fotos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)