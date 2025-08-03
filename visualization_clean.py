"""
Módulo de visualização limpo usando apenas Matplotlib.
"""
from typing import List, Dict, Any, Optional, Callable, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches

class Config:
    """Configurações globais do módulo de visualização."""
    
    # Cores em formato RGB normalizado (0-1)
    BRANCO = (1.0, 1.0, 1.0)
    PRETO = (0.0, 0.0, 0.0)
    CINZA_CLARO = (0.94, 0.94, 0.94)
    CINZA = (0.78, 0.78, 0.78)
    VERMELHO = (1.0, 0.39, 0.39)
    VERDE = (0.39, 0.78, 0.39)
    AZUL = (0.39, 0.39, 1.0)
    AMARELO = (1.0, 1.0, 0.39)
    LARANJA = (1.0, 0.65, 0.0)
    
    # Dimensões da figura (reduzidas para células menores)
    LARGURA_FIGURA = 12  # polegadas (reduzido para células menores)
    ALTURA_FIGURA = 7    # polegadas (reduzido para células menores)
    
    # Configurações da grade
    MARGEM = 0.02        # Reduzido para usar mais espaço
    ESPACO_CELULAS = 0.02  # Reduzido para diminuir o espaço entre células
    
    # Configurações dos gráficos
    ALTURA_GRAFICO = 0.3  # Gráficos mais compactos
    ESPACO_ENTRE_GRAFICOS = 0.05  # Menos espaço entre gráficos
    
    # Cores adicionais
    CINZA_ESCURO = (0.39, 0.39, 0.39)
    AZUL_ESCURO = (0.0, 0.0, 0.78)
    VERMELHO_ESCURO = (0.78, 0.0, 0.0)
    VERDE_ESCURO = (0.0, 0.59, 0.0)
    
    # Constantes para a grade
    DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    HORARIOS = ['08:00-10:00', '10:00-12:00', '13:30-15:30', '15:30-17:30']

# Variáveis globais
fig = None
ax_grade = None
ax_evolucao = None
ax_distribuicao = None
melhor_fitness_historico = []

class EstatisticasPopulacao:
    """Classe para rastrear estatísticas da população."""
    def __init__(self):
        self.geracoes = []
        self.melhores_fitness = []
        self.medias_fitness = []
        self.piores_fitness = []
        self.max_historico = 100
        self.ultima_populacao = []

    def adicionar_geracao(self, geracao: int, populacao: List[Any], calcular_fitness_func) -> None:
        """Adiciona estatísticas da geração atual."""
        if not populacao:
            return
            
        try:
            fitness_values = [calcular_fitness_func(ind) for ind in populacao]
            self.ultima_populacao = populacao
            
            self.geracoes.append(geracao)
            self.melhores_fitness.append(max(fitness_values))
            self.medias_fitness.append(sum(fitness_values) / len(fitness_values))
            self.piores_fitness.append(min(fitness_values))
            
            # Limita o histórico ao tamanho máximo
            if len(self.geracoes) > self.max_historico:
                self.geracoes.pop(0)
                self.melhores_fitness.pop(0)
                self.medias_fitness.pop(0)
                self.piores_fitness.pop(0)
                
        except Exception as e:
            print(f"Erro ao adicionar geração: {e}")

estatisticas = EstatisticasPopulacao()

def inicializar_visualizacao() -> bool:
    """Inicializa a visualização com Matplotlib."""
    global fig, ax_grade, ax_evolucao, ax_distribuicao
    
    try:
        if fig is not None:
            plt.close(fig)
        
        # Cria uma figura menor para a grade
        fig = plt.figure(figsize=(18, 8))
        
        # Ajusta o GridSpec para dar mais espaço para os gráficos
        gs = GridSpec(2, 2, 
                     width_ratios=[2, 1],  # Menos espaço para a grade
                     height_ratios=[1, 1],
                     wspace=0.1,    # Mais espaço entre subplots
                     hspace=0.15,   # Espaço vertical
                     left=0.05, right=0.95,  # Margens laterais
                     top=0.9, bottom=0.1)   # Margens superior e inferior
        
        ax_grade = fig.add_subplot(gs[:, 0])
        ax_evolucao = fig.add_subplot(gs[0, 1])
        ax_distribuicao = fig.add_subplot(gs[1, 1])
        
        # Configura títulos com fonte maior
        ax_grade.set_title('Grade Horária', fontsize=14, pad=12)
        ax_evolucao.set_title('Evolução do Fitness', fontsize=14, pad=10)
        ax_distribuicao.set_title('Distribuição de Fitness', fontsize=14, pad=10)
        
        plt.tight_layout()
        plt.ion()
        plt.show(block=False)
        
        return True
        
    except Exception as e:
        print(f"Erro ao inicializar a visualização: {e}")
        return False

def desenhar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float) -> None:
    """Desenha a grade horária."""
    global ax_grade
    
    if ax_grade is None:
        inicializar_visualizacao()
    
    ax_grade.clear()
    
    # Configurações iniciais
    num_dias = len(Config.DIAS)
    num_horarios = len(Config.HORARIOS)
    
    # Desenha o fundo da grade
    for i in range(num_dias):
        for j in range(num_horarios):
            cor = Config.CINZA_CLARO if (i + j) % 2 == 0 else Config.BRANCO
            ax_grade.add_patch(patches.Rectangle(
                (i, j), 1, 1, 
                facecolor=cor,
                edgecolor=Config.PRETO,
                linewidth=1
            ))
    
    # Adiciona os cabeçalhos dos dias
    for i, dia in enumerate(Config.DIAS):
        ax_grade.text(i + 0.5, -0.1, dia, 
                     ha='center', va='center', 
                     fontweight='bold')
    
    # Adiciona os horários
    for j, horario in enumerate(Config.HORARIOS):
        ax_grade.text(-0.01, j + 0.5, horario, 
                     ha='right', va='center', 
                     fontweight='bold')
    
    # Adiciona as aulas
    for aula in grade:
        try:
            dia_idx = Config.DIAS.index(aula['dia'])
            horario_idx = Config.HORARIOS.index(aula['horario'])
            
            # Escolhe a cor com base no tipo de sala
            cor = Config.AZUL if 'Lab.' in aula['sala'] else Config.VERDE
            
            # Desenha o retângulo da aula
            ax_grade.add_patch(patches.Rectangle(
                (dia_idx, horario_idx), 1, 1,
                facecolor=cor,
                edgecolor=Config.PRETO,
                alpha=1,
                linewidth=1
            ))
            
            # Adiciona o texto da disciplina, professor e sala com formatação otimizada
            disciplina = aula['disciplina'].split()
            # Quebra o texto em linhas menores
            linhas = []
            linha_atual = []
            for palavra in disciplina:
                if len(' '.join(linha_atual + [palavra])) <= 12:  
                    linha_atual.append(palavra)
                else:
                    linhas.append(' '.join(linha_atual))
                    linha_atual = [palavra]
            if linha_atual:
                linhas.append(' '.join(linha_atual))
            
            # Adiciona o professor e a sala em linhas separadas
            texto = '\n'.join(linhas) + f"\nProf: {aula.get('professor', 'N/A')}\n{aula['sala']}"
            
            ax_grade.text(dia_idx + 0.5, horario_idx + 0.5, texto,
                        ha='center', va='center',
                        fontsize=8, wrap=True,  # Fonte um pouco menor para caber mais informações
                        bbox=dict(facecolor='white', alpha=0.7, 
                                edgecolor='none', pad=0.2,  # Padding reduzido
                                boxstyle='round,pad=0.1'))  # Borda mais fina
                        
        except (ValueError, KeyError) as e:
            print(f"Aviso: Erro ao desenhar aula {aula.get('disciplina', 'desconhecida')}: {e}")
    
    # Configura os eixos para preencher o espaço disponível
    ax_grade.set_xlim(-0.1, num_dias + 0.1)
    ax_grade.set_ylim(num_horarios + 0.1, -0.1)  # Inverte o eixo Y para ter Segunda em cima
    ax_grade.axis('off')
    
    # Ajusta o tamanho da fonte e o layout
    plt.rcParams.update({
        'font.size': 11.0,  # Tamanho da fonte aumentado
        'axes.titlesize': 10,  # Títulos maiores
        'axes.labelsize': 10,  # Rótulos dos eixos maiores
        'xtick.labelsize': 10,  # Tamanho dos ticks do eixo X
        'ytick.labelsize': 10,  # Tamanho dos ticks do eixo Y
        'legend.fontsize': 9,  # Tamanho da legenda
    })
    
    # Ajuste fino do layout
    plt.subplots_adjust(
        left=0, right=1.5,  # Margens laterais ajustadas
        top=0.9, bottom=0.1,    # Margens superior e inferior
        wspace=0.5, hspace=0.5  # Espaçamento entre subplots
    )
    
    # Adiciona o título com fonte maior
    ax_grade.set_title(f'Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}', 
                      fontsize=12, pad=10)

def atualizar_graficos(populacao: List[Dict[str, Any]], calcular_fitness_func: Callable) -> None:
    """Atualiza os gráficos de evolução e distribuição."""
    global ax_evolucao, ax_distribuicao, melhor_fitness_historico
    
    if ax_evolucao is None or ax_distribuicao is None:
        return
    
    # Atualiza o gráfico de evolução
    ax_evolucao.clear()
    
    if estatisticas.geracoes:
        ax_evolucao.plot(estatisticas.geracoes, estatisticas.melhores_fitness, 'g-', label='Melhor')
        ax_evolucao.plot(estatisticas.geracoes, estatisticas.medias_fitness, 'b-', label='Média')
        ax_evolucao.plot(estatisticas.geracoes, estatisticas.piores_fitness, 'r-', label='Pior')
        ax_evolucao.legend()
        ax_evolucao.set_xlabel('Geração')
        ax_evolucao.set_ylabel('Fitness')
        ax_evolucao.grid(True, alpha=0.3)
    
    # Atualiza o gráfico de distribuição
    ax_distribuicao.clear()
    
    if populacao and calcular_fitness_func:
        try:
            fitness_values = [calcular_fitness_func(ind) for ind in populacao]
            ax_distribuicao.hist(fitness_values, bins=20, color=Config.AZUL, alpha=0.7)
            ax_distribuicao.set_xlabel('Fitness')
            ax_distribuicao.set_ylabel('Frequência')
            ax_distribuicao.grid(True, alpha=0.3)
        except Exception as e:
            print(f"Erro ao atualizar gráfico de distribuição: {e}")

def visualizar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float, 
                   populacao: List[Dict[str, Any]] = None, 
                   calcular_fitness_func: Callable = None,
                   fechar_ao_terminar: bool = False,
                   mostrar_evolucao: bool = True) -> bool:
    """
    Atualiza a visualização da grade e dos gráficos.
    
    Args:
        grade: Lista de dicionários representando a grade horária.
        geracao: Número da geração atual.
        fitness: Valor de fitness da melhor solução.
        populacao: Lista da população atual (opcional).
        calcular_fitness_func: Função para calcular o fitness (opcional).
        fechar_ao_terminar: Se True, fecha a janela após exibir.
        mostrar_evolucao: Se True, mostra os gráficos de evolução.
        
    Returns:
        True se a visualização foi atualizada com sucesso, False caso contrário.
    """
    try:
        global fig, ax_grade, ax_evolucao, ax_distribuicao
        
        # Inicializa se necessário
        if fig is None or not plt.fignum_exists(fig.number):
            if not inicializar_visualizacao():
                return False
        
        # Atualiza as estatísticas
        if populacao is not None and calcular_fitness_func is not None:
            estatisticas.adicionar_geracao(geracao, populacao, calcular_fitness_func)
        
        # Desenha a grade
        desenhar_grade(grade, geracao, fitness)
        
        # Atualiza os gráficos se necessário
        if mostrar_evolucao and populacao is not None and calcular_fitness_func is not None:
            atualizar_graficos(populacao, calcular_fitness_func)
        
        # Atualiza a figura
        plt.draw()
        plt.pause(0.01)
        
        return True
        
    except Exception as e:
        print(f"Erro na visualização: {e}")
        return False

def salvar_imagem_grade(grade: List[Dict[str, Any]], caminho: str, 
                       geracao: int, fitness: float) -> None:
    """
    Salva a grade horária como uma imagem.
    
    Args:
        grade: Lista de dicionários representando a grade horária.
        caminho: Caminho para salvar a imagem.
        geracao: Número da geração.
        fitness: Valor de fitness da solução.
    """
    try:
        # Cria uma nova figura apenas para a grade
        fig_temp, ax_temp = plt.subplots(figsize=(10, 6))
        
        # Salva a visualização atual
        desenhar_grade(grade, geracao, fitness)
        
        # Salva a figura
        plt.savefig(caminho, bbox_inches='tight', dpi=300)
        plt.close(fig_temp)
        
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")

def finalizar_visualizacao() -> None:
    """Finaliza a visualização corretamente."""
    global fig
    
    try:
        if fig is not None:
            plt.close(fig)
            fig = None
    except Exception as e:
        print(f"Erro ao finalizar a visualização: {e}")
    finally:
        plt.close('all')
