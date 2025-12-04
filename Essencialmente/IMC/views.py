from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from .models import AvaliacaoIMC, classificar_imc 
from .forms import AvaliarIMCForm 

def index(request):
    """View simples para renderizar a página inicial."""
    # O DJANGO VAI PROCURAR ESSE ARQUIVO DENTRO DE templates/IMC/index.html
    return render(request, 'IMC/index.html')

# --- FUNÇÃO AUXILIAR CORRIGIDA PARA BOOTSTRAP ---
def obter_cor_classificacao(classificacao):
    """Define a classe de cor do Bootstrap baseada na classificação."""
    if 'Abaixo' in classificacao:
        return 'text-warning fw-bold' # Amarelo (Bootstrap)
    elif 'Normal' in classificacao:
        return 'text-success fw-bold' # Verde (Bootstrap)
    elif 'Sobrepeso' in classificacao:
        return 'text-warning fw-bold' # Amarelo/Laranja (Bootstrap)
    elif 'Obesidade' in classificacao:
        return 'text-danger fw-bold'  # Vermelho (Bootstrap)
    return 'text-secondary' # Cinza (Padrão)

class Avaliar_IMC_View(View):
    template_name = 'IMC/Avaliacao_IMC.html'
    
    def get(self, request, *args, **kwargs):
        """Exibe o formulário vazio."""
        form = AvaliarIMCForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Processa o cálculo e salva no banco."""
        form = AvaliarIMCForm(request.POST, request.FILES)
        
        # Variáveis de contexto inicial
        valor_imc_calculado = None
        classificacao_calculada = None
        cor_classificacao = None
        
        if form.is_valid():
            try:
                # Cria o objeto mas não salva ainda no banco
                avaliacao = form.save(commit=False)
                
                # Garante o cálculo para exibição imediata na tela
                if avaliacao.altura > 0:
                    valor_imc = avaliacao.peso / (avaliacao.altura ** 2)
                    valor_imc_calculado = round(valor_imc, 2)
                    
                    # Usa a função importada do models.py ou calcula aqui
                    classificacao_calculada = classificar_imc(valor_imc)
                    cor_classificacao = obter_cor_classificacao(classificacao_calculada)

                    # Salva definitivamente
                    avaliacao.save()
                    
                    messages.success(request, f'Cadastro realizado! IMC: {valor_imc_calculado}')
                    
                    # Limpa o formulário para um novo cadastro
                    form = AvaliarIMCForm()
                else:
                    form.add_error('altura', 'A altura deve ser maior que zero.')
                    
            except Exception as e:
                messages.error(request, f'Erro ao salvar: {e}')
        else:
            messages.error(request, 'O formulário contém erros. Verifique os campos.')

        # Renderiza a página novamente com o resultado
        contexto = {
            'form': form,
            'valor_imc': valor_imc_calculado,
            'classificacao': classificacao_calculada,
            'cor_classificacao': cor_classificacao,
        }
        return render(request, self.template_name, contexto)


class ListarCadastradosIMC_View(ListView):
    """Lista todos os cadastros com paginação."""
    model = AvaliacaoIMC
    template_name = 'IMC/ListarCadastradosIMC.html'
    context_object_name = 'avaliacoes'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        """Injeta a cor da classificação em cada item da lista."""
        context = super().get_context_data(**kwargs)
        
        # Processamento extra para exibir as cores na tabela
        for avaliacao in context['avaliacoes']:
            # Assume que seu model tem a property @valor_imc
            # Se der erro aqui, usamos o calculo manual: imc = avaliacao.peso / (avaliacao.altura ** 2)
            imc = avaliacao.valor_imc 
            classificacao = classificar_imc(imc)
            
            # Adiciona atributos dinâmicos ao objeto (apenas para o template)
            avaliacao.classificacao_texto = classificacao
            avaliacao.cor_classificacao = obter_cor_classificacao(classificacao)
            
        return context