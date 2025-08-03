"""
Módulo de visualização usando Matplotlib para exibir a grade horária e gráficos de evolução.
"""
from typing import List, Dict, Any, Optional, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches

# Variáveis globais para manter o estado da visualização
fig = None
ax_grade = None
ax_evolucao = None
ax_distribuicao = None

class VisualizacaoGrade:
    """Classe para gerenciar a visualização da grade horária e dos gráficos."""
    
    def __init__(self):
        """Inicializa a visualização."""
        self.fig = None
        self.ax_grade = None
        self.ax_evolucao = None
        self.ax_distribuicao = None
        self.historico_fitness = []
        self.melhor_fitness_por_geracao = []
        self.inicializada = False
    
    def inicializar(self):
        """Inicializa a janela de visualização."""
        # Fecha a figura anterior se existir
        if self.fig is not None:
            plt.close(self.fig)
        
        # Cria uma nova figura com dois subplots lado a lado
        self.fig = plt.figure(figsize=(16, 8))
        gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])
        
        # Cria os subplots
        self.ax_grade = self.fig.add_subplot(gs[:, 0])  # Grade ocupa a coluna inteira à esquerda
        self.ax_evolucao = self.fig.add_subplot(gs[0, 1])  # Gráfico de evolução
        self.ax_distribuicao = self.fig.add_subplot(gs[1, 1])  # Gráfico de distribuição
        
        # Configurações iniciais dos eixos
        self.ax_grade.set_title('Grade Horária')
        self.ax_evolucao.set_title('Evolução do Fitness')
        self.ax_distribuicao.set_title('Distribuição de Fitness')
        
        # Ajusta o layout
        plt.tight_layout()
        plt.ion()  # Modo interativo
        plt.show(block=False)
        self.inicializada = True
    
    def atualizar(self, grade: List[Dict[str, Any]], geracao: int, fitness: float,
                 populacao: Optional[List[Dict[str, Any]]] = None,
                 calcular_fitness_func: Optional[Callable] = None) -> bool:
        """
        Atualiza a visualização com os dados mais recentes.
        
        Args:
            grade: Lista de dicionários representando a grade horária.
            geracao: Número da geração atual.
            fitness: Valor de fitness da melhor solução.
            populacao: Lista da população atual (opcional).
            calcular_fitness_func: Função para calcular o fitness (opcional).
            
        Returns:
            True se a visualização foi atualizada com sucesso, False caso contrário.
        """
        try:
            # Inicializa se necessário
            if not self.inicializada:
                self.inicializar()
            
            # Atualiza o título da figura
            self.fig.suptitle(f'Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}')
            
            # Limpa os eixos
            self.ax_grade.clear()
            self.ax_evolucao.clear()
            self.ax_distribuicao.clear()
            
            # Desenha a grade horária
            self._desenhar_grade(grade)
            
            # Se houver população, desenha os gráficos de evolução
            if populacao is not None and calcular_fitness_func is not None:
                self._atualizar_graficos(populacao, calcular_fitness_func)
            
            # Ajusta o layout e desenha
            plt.tight_layout()
            plt.draw()
            plt.pause(0.01)  # Pequena pausa para permitir a atualização
            
            return True
            
        except Exception as e:
            print(f"Erro na visualização: {e}")
            return False
    
    def _desenhar_grade(self, grade: List[Dict[str, Any]]):
        """Desenha a grade horária."""
        # Configurações iniciais
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        horarios = ['08:00-10:00', '10:00-12:00', '13:30-15:30', '15:30-17:30']
        
        # Cria a grade vazia
        self.ax_grade.set_xticks(np.arange(len(dias)) + 0.5)
        self.ax_grade.set_yticks(np.arange(len(horarios)) + 0.5)
        self.ax_grade.set_xticklabels(dias)
        self.ax_grade.set_yticklabels(horarios)
        self.ax_grade.grid(True, linestyle='-', color='black', alpha=0.3)
        
        # Preenche as células com as aulas
        for aula in grade:
            try:
                dia_idx = dias.index(aula['dia'])
                horario_idx = horarios.index(aula['horario'])
                
                # Cores diferentes para diferentes tipos de sala
                cor = 'lightblue' if 'Lab.' in aula['sala'] else 'lightgreen'
                
                # Desenha o retângulo da célula
                rect = patches.Rectangle(
                    (dia_idx, horario_idx), 1, 1, 
                    linewidth=1, edgecolor='black', 
                    facecolor=cor, alpha=0.7
                )
                self.ax_grade.add_patch(rect)
                
                # Adiciona o texto da disciplina
                texto = f"{aula['disciplina']}\n{aula['sala']}"
                self.ax_grade.text(dia_idx + 0.5, horario_idx + 0.5, texto, 
                               ha='center', va='center', fontsize=8, wrap=True)
            except (ValueError, KeyError) as e:
                print(f"Aviso: Erro ao desenhar aula {aula.get('disciplina', 'desconhecida')}: {e}")
        
        self.ax_grade.set_title('Grade Horária')
        self.ax_grade.set_xlim(0, len(dias))
        self.ax_grade.set_ylim(0, len(horarios))
    
    def _atualizar_graficos(self, populacao: List[Dict[str, Any]], 
                          calcular_fitness_func: Callable):
        """Atualiza os gráficos de evolução e distribuição."""
        # Calcula os valores de fitness da população
        valores_fitness = [calcular_fitness_func(individuo) for individuo in populacao]
        
        # Atualiza o histórico
        self.historico_fitness.extend(valores_fitness)
        self.melhor_fitness_por_geracao.append(max(valores_fitness))
        
        # Gráfico de evolução (linha superior direita)
        self.ax_evolucao.plot(self.melhor_fitness_por_geracao, 'b-')
        self.ax_evolucao.set_title('Evolução do Melhor Fitness')
        self.ax_evolucao.set_xlabel('Geração')
        self.ax_evolucao.set_ylabel('Fitness')
        self.ax_evolucao.grid(True, linestyle='--', alpha=0.7)
        
        # Gráfico de distribuição (linha inferior direita)
        self.ax_distribuicao.hist(valores_fitness, bins=20, alpha=0.7, color='green')
        self.ax_distribuicao.set_title('Distribuição de Fitness')
        self.ax_distribuicao.set_xlabel('Fitness')
        self.ax_distribuicao.set_ylabel('Frequência')
        self.ax_distribuicao.grid(True, linestyle='--', alpha=0.7)
    
    def manter_aberto(self):
        """Mantém a janela aberta até que o usuário a feche."""
        if self.inicialized:
            plt.ioff()  # Desativa o modo interativo
            plt.show()

# Instância global para uso no módulo
visualizador = VisualizacaoGrade()

def visualizar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float,
                   populacao: Optional[List[Dict[str, Any]]] = None,
                   calcular_fitness_func: Optional[Callable] = None,
                   fechar_ao_terminar: bool = False,
                   mostrar_evolucao: bool = True) -> bool:
    """
    Função de conveniência para atualizar a visualização.
    
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
    if not mostrar_evolucao or populacao is None or calcular_fitness_func is None:
        # Se não for para mostrar a evolução, usa apenas a grade
        return visualizador.atualizar(grade, geracao, fitness)
    else:
        return visualizador.atualizar(grade, geracao, fitness, populacao, calcular_fitness_func)

def finalizar_visualizacao():
    """Finaliza a visualização corretamente."""
    plt.ioff()
    plt.close('all')

def salvar_imagem_grade(grade: List[Dict[str, Any]], caminho: str, 
                       geracao: int, fitness: float):
    """
    Salva a grade horária como uma imagem.
    
    Args:
        grade: Lista de dicionários representando a grade horária.
        caminho: Caminho para salvar a imagem.
        geracao: Número da geração.
        fitness: Valor de fitness da solução.
    """
    # Cria uma nova figura apenas para a grade
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Desenha a grade
    visualizador._desenhar_grade(grade)
    fig.suptitle(f'Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}')
    
    # Ajusta o layout e salva
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)
