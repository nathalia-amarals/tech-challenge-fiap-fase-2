"""
Módulo de visualização para o algoritmo genético de grade horária.

Este módulo fornece funções para visualização interativa da grade horária usando Pygame,
incluindo exibição em tempo real, salvamento de imagens e controle de visualização.
"""
import os
import pygame
from typing import List, Dict, Any, Optional, Final, Tuple
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches

class EstatisticasPopulacao:
    """
    Classe para rastrear estatísticas da população ao longo das gerações.
    """
    def __init__(self):
        self.geracoes = []
        self.melhores_fitness = []
        self.medias_fitness = []
        self.piores_fitness = []
        self.max_historico = 100  # Número máximo de gerações a serem armazenadas
    
    def adicionar_geracao(self, geracao: int, populacao: List[Any], calcular_fitness_func) -> None:
        """
        Adiciona as estatísticas da geração atual.
        
        Args:
            geracao: Número da geração atual
            populacao: Lista de indivíduos da população
            calcular_fitness_func: Função para calcular o fitness de um indivíduo
            
        Raises:
            TypeError: Se a população não for uma lista
            ValueError: Se a população estiver vazia ou contiver itens inválidos
        """
        if not isinstance(populacao, list):
            raise TypeError(f"A população deve ser uma lista, mas recebido: {type(populacao)}")
            
        if not populacao:
            print("Aviso: População vazia, nenhuma estatística será adicionada.")
            return
            
        try:
            # Garante que cada indivíduo é um dicionário antes de calcular o fitness
            if not all(isinstance(ind, (dict, list)) for ind in populacao):
                raise ValueError("A população deve conter apenas dicionários ou listas")
                
            # Calcula as estatísticas de fitness
            fitness_populacao = []
            for i, individuo in enumerate(populacao):
                try:
                    fitness = calcular_fitness_func(individuo)
                    if not isinstance(fitness, (int, float)):
                        print(f"Aviso: Fitness inválido para o indivíduo {i}: {fitness}")
                        continue
                    fitness_populacao.append(fitness)
                except Exception as e:
                    print(f"Erro ao calcular fitness do indivíduo {i}: {e}")
                    continue
            
            if not fitness_populacao:
                print("Aviso: Nenhum fitness válido para calcular estatísticas")
                return
                
            melhor = max(fitness_populacao)
            pior = min(fitness_populacao)
            media = sum(fitness_populacao) / len(fitness_populacao)
            
            # Adiciona às listas
            self.geracoes.append(geracao)
            self.melhores_fitness.append(melhor)
            self.medias_fitness.append(media)
            self.piores_fitness.append(pior)
            
            # Mantém apenas o histórico mais recente
            if len(self.geracoes) > self.max_historico:
                self.geracoes.pop(0)
                self.melhores_fitness.pop(0)
                self.medias_fitness.pop(0)
                self.piores_fitness.pop(0)
                
        except Exception as e:
            print(f"Erro ao processar estatísticas da geração {geracao}: {e}")
            import traceback
            traceback.print_exc()
    
    def limpar(self) -> None:
        """Limpa todas as estatísticas armazenadas."""
        self.geracoes.clear()
        self.melhores_fitness.clear()
        self.medias_fitness.clear()
        self.piores_fitness.clear()

class Config:
    """Configurações globais do módulo de visualização."""
    # Cores
    BRANCO: Final[tuple[int, int, int]] = (255, 255, 255)
    PRETO: Final[tuple[int, int, int]] = (0, 0, 0)
    CINZA_CLARO: Final[tuple[int, int, int]] = (240, 240, 240)
    CINZA: Final[tuple[int, int, int]] = (200, 200, 200)
    VERMELHO: Final[tuple[int, int, int]] = (255, 100, 100)
    VERDE: Final[tuple[int, int, int]] = (100, 200, 100)
    AZUL: Final[tuple[int, int, int]] = (100, 100, 255)
    AMARELO: Final[tuple[int, int, int]] = (255, 255, 100)
    LARANJA: Final[tuple[int, int, int]] = (255, 165, 0)

    # Configurações da janela
    LARGURA_JANELA: Final[int] = 1600  # Largura total da janela
    ALTURA_JANELA: Final[int] = 900   # Altura total da janela
    MARGEM: Final[int] = 20           # Margem entre as seções
    
    # Configurações da grade
    LARGURA_CELULA: Final[int] = 180
    ALTURA_CABECALHO: Final[int] = 40
    ALTURA_CELULA: Final[int] = 140
    
    # Configurações dos gráficos
    ALTURA_GRAFICO: Final[int] = 350
    ESPACO_ENTRE_GRAFICOS: Final[int] = 20
    
    # Cores adicionais
    CINZA_ESCURO: Final[tuple[int, int, int]] = (100, 100, 100)
    AZUL_ESCURO: Final[tuple[int, int, int]] = (0, 0, 200)
    VERMELHO_ESCURO: Final[tuple[int, int, int]] = (200, 0, 0)
    VERDE_ESCURO: Final[tuple[int, int, int]] = (0, 150, 0)
    
    # Taxa de atualização
    FPS: Final[int] = 30

    # Dias da semana e horários
    DIAS: Final[list[str]] = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    HORARIOS: Final[list[str]] = ['08:00-10:00', '10:00-12:00', '13:30-15:30', '15:30-17:30']

# Variáveis de estado do módulo
pygame_initialized: bool = False
janela_grade: Optional[pygame.Surface] = None
janela_graficos: Optional[pygame.Surface] = None
fonte_pequena: Optional[pygame.font.Font] = None
fonte_media: Optional[pygame.font.Font] = None
fonte_grande: Optional[pygame.font.Font] = None
estatisticas = EstatisticasPopulacao()
janela_graficos_visivel: bool = True

def carregar_fontes() -> bool:
    """
    Carrega e configura as fontes necessárias para a renderização.
    
    Returns:
        bool: True se as fontes foram carregadas com sucesso, False caso contrário.
    """
    global fonte_pequena, fonte_media, fonte_grande
    
    try:
        # Tenta carregar a fonte Arial primeiro
        fonte_pequena = pygame.font.SysFont('Arial', 10)
        fonte_media = pygame.font.SysFont('Arial', 14)
        fonte_grande = pygame.font.SysFont('Arial', 18, bold=True)
        
        # Testa se as fontes foram carregadas corretamente
        if not all([fonte_pequena, fonte_media, fonte_grande]):
            raise Exception("Falha ao carregar fontes Arial")
            
        return True
        
    except Exception as e:
        print(f"Aviso: {e}. Tentando fonte padrão do sistema...")
        try:
            # Tenta obter a fonte padrão do sistema
            fonte_padrao = pygame.font.get_default_font()
            fonte_pequena = pygame.font.SysFont(fonte_padrao, 10)
            fonte_media = pygame.font.SysFont(fonte_padrao, 14)
            fonte_grande = pygame.font.SysFont(fonte_padrao, 18, bold=True)
            
            if not all([fonte_pequena, fonte_media, fonte_grande]):
                raise Exception("Falha ao carregar fontes padrão do sistema")
                
            return True
            
        except Exception as e2:
            print(f"Erro crítico: Não foi possível carregar nenhuma fonte: {e2}")
            return False

def inicializar_pygame() -> bool:
    """
    Inicializa o Pygame e configura o ambiente de renderização.
    
    Esta função é responsável por:
    1. Inicializar o Pygame e o módulo de fontes
    2. Carregar as fontes necessárias
    3. Criar a janela de exibição
    
    Returns:
        bool: True se a inicialização foi bem-sucedida, False caso contrário.
    """
    global pygame_initialized, fonte_pequena, fonte_media, fonte_grande, janela_grade
    
    try:
        if not pygame_initialized:
            pygame.init()
            pygame.font.init()
            pygame_initialized = True
        
        # Carrega as fontes primeiro
        if not carregar_fontes():
            return False
        
        # Configuração da janela única
        os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
        global janela_grade
        janela_grade = pygame.display.set_mode((Config.LARGURA_JANELA, Config.ALTURA_JANELA), pygame.RESIZABLE)
        pygame.display.set_caption("Grade Horária e Gráficos - Algoritmo Genético")
        
        return True
        
    except Exception as e:
        print(f"Erro ao inicializar o Pygame: {e}")
        pygame_initialized = False
        return False

def normalize_time(time_str: str) -> str:
    """Normaliza a string de horário removendo espaços extras e garantindo formato consistente."""
    if not time_str:
        return ""
    return time_str.strip()

def desenhar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float, x: int = 0, y: int = 0, largura: int = None, altura: int = None) -> None:
    """
    Renderiza a grade horária na janela do Pygame.
    
    Esta função é responsável por desenhar todos os elementos visuais da grade horária,
    incluindo cabeçalhos, linhas de grade e informações das aulas. Ela também exibe
    informações de depuração no console quando necessário.
    
    Args:
        grade: Lista de dicionários contendo as informações das aulas, onde cada
            dicionário deve conter as chaves: 'disciplina', 'sala', 'professor',
            'dia' e 'horario'.
        geracao: Número da geração atual do algoritmo genético.
        fitness: Valor de fitness da grade atual (0.0 a 1.0).
        x: Posição X do canto superior esquerdo da grade.
        y: Posição Y do canto superior esquerdo da grade.
        largura: Largura total da área de desenho.
        altura: Altura total da área de desenho.
        
    Notas:
        - A função assume que o Pygame já foi inicializado e que a janela foi criada.
        - As dimensões da grade são calculadas com base nos parâmetros fornecidos.
    """
    global janela_grade, fonte_pequena, fonte_media, fonte_grande
    
    # Usa as dimensões fornecidas ou as padrão da janela
    if largura is None:
        largura = Config.LARGURA_JANELA // 2 - Config.MARGEM // 2
    if altura is None:
        altura = Config.ALTURA_JANELA
    
    # Limpa a tela
    janela_grade.fill(Config.BRANCO)
    
    # Título da grade
    titulo = f"Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}"
    titulo_surface = fonte_grande.render(titulo, True, Config.PRETO)
    janela_grade.blit(titulo_surface, (x + (largura - titulo_surface.get_width()) // 2, y + 10))
    
    # Desenha os cabeçalhos dos dias
    for i, dia in enumerate(Config.DIAS):
        x = Config.MARGEM + (i * Config.LARGURA_CELULA)
        y = Config.MARGEM + 40
        
        # Cabeçalho do dia
        pygame.draw.rect(janela_grade, Config.CINZA_CLARO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CABECALHO))
        pygame.draw.rect(janela_grade, Config.PRETO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CABECALHO), 1)
        
        # Texto do dia
        dia_surface = fonte_media.render(dia, True, Config.PRETO)
        janela_grade.blit(dia_surface, (x + Config.MARGEM + (Config.LARGURA_CELULA // 2) - (dia_surface.get_width() // 2), y + Config.ALTURA_CABECALHO // 2 - 10))
    
    # Desenha os horários e linhas horizontais
    for i, horario in enumerate(Config.HORARIOS):
        y = Config.MARGEM + Config.ALTURA_CABECALHO + 40 + (i * Config.ALTURA_CELULA)
        
        # Texto do horário
        horario_surface = fonte_pequena.render(horario, True, Config.PRETO)
        janela_grade.blit(horario_surface, (x + Config.MARGEM // 2 - horario_surface.get_width() // 2, y + 5))
        
        # Linha horizontal
        pygame.draw.line(janela_grade, Config.CINZA, 
                       (Config.MARGEM, y), 
                       (largura - Config.MARGEM, y), 1)
    
    # Desenha as linhas verticais
    for i in range(len(Config.DIAS) + 1):
        x = Config.MARGEM + (i * Config.LARGURA_CELULA)
        y_inicio = Config.MARGEM + Config.ALTURA_CABECALHO + 40
        y_fim = y_inicio + (len(Config.HORARIOS) * Config.ALTURA_CELULA)
        pygame.draw.line(janela_grade, Config.CINZA, (x, y_inicio), (x, y_fim), 1)
    
    # Mapeamento de horários para índices
    horario_para_indice = {horario: idx for idx, horario in enumerate(Config.HORARIOS)}
    
    # Mapeamento de dias para índices
    dia_para_indice = {dia: idx for idx, dia in enumerate(Config.DIAS)}
    
    # Desenha as aulas na grade
    for aula in grade:
        try:
            # Obtém as informações da aula
            disciplina = aula.get('disciplina', 'Desconhecida')
            sala = aula.get('sala', 'Desconhecida')
            professor = aula.get('professor', 'Desconhecido')
            
            # Normaliza o dia e o horário
            dia = str(aula.get('dia', '')).strip().capitalize()
            horario = normalize_time(str(aula.get('horario', '')))
            
            # Verifica se o dia e o horário são válidos
            if not dia or not horario:
                print(f"Aviso: Aula sem dia ou horário: {aula}")
                continue
                
            if dia not in dia_para_indice:
                print(f"Aviso: Dia inválido: '{dia}'. Aula: {aula}")
                continue
                
            if horario not in horario_para_indice:
                print(f"Aviso: Horário inválido: '{horario}'. Aula: {aula}")
                continue
            
            # Calcula a posição da célula
            x = Config.MARGEM + (dia_para_indice[dia] * Config.LARGURA_CELULA)
            y = Config.MARGEM + Config.ALTURA_CABECALHO + 40 + (horario_para_indice[horario] * Config.ALTURA_CELULA)
            
            # Define a cor com base no tipo de sala
            cor = Config.AMARELO if 'lab' in sala.lower() else Config.AZUL
            
            # Desenha a célula da aula
            pygame.draw.rect(janela_grade, cor, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA))
            pygame.draw.rect(janela_grade, Config.PRETO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA), 1)
            
            # Quebra o texto da disciplina em várias linhas se necessário
            palavras = disciplina.split()
            linhas = []
            linha_atual = []
            
            for palavra in palavras:
                linha_teste = ' '.join(linha_atual + [palavra])
                texto_teste = fonte_pequena.render(linha_teste, True, Config.PRETO)
                
                if texto_teste.get_width() > Config.LARGURA_CELULA - 20:  # Margem de 10px de cada lado
                    fonte_pequena = pygame.font.SysFont("Arial", 10)
                else:
                    if linha_atual:
                        linhas.append(' '.join(linha_atual))
                    linha_atual = [palavra]
            
            if linha_atual:
                linhas.append(' '.join(linha_atual))
            
            # Desenha o texto da disciplina (máximo de 3 linhas)
            for i, linha in enumerate(linhas[:3]):  # Máximo de 3 linhas para a disciplina
                if (i * 15) < Config.ALTURA_CELULA - 30:  # Deixa espaço para sala e professor
                    text_surface = fonte_pequena.render(linha, True, Config.PRETO)
                    janela_grade.blit(text_surface, (x + 10, y + 5 + i * (fonte_pequena.get_height() + 2)))
            
            try:
                # Usa uma fonte ligeiramente menor para sala e professor
                fonte_pequena = pygame.font.SysFont('Arial', 9)
                
                # Trunca textos longos para caber na célula
                sala_text = f"Sala: {sala}" if len(sala) < 15 else f"Sala: {sala[:12]}..."
                prof_text = f"Prof: {professor}" if len(professor) < 15 else f"Prof: {professor[:12]}..."
                
                # Renderiza sala e professor
                sala_surface = fonte_pequena.render(sala_text, True, Config.PRETO)
                prof_surface = fonte_pequena.render(prof_text, True, Config.PRETO)
                janela_grade.blit(sala_surface, (x + 10, y + Config.ALTURA_CELULA - 30))
                janela_grade.blit(prof_surface, (x + 10, y + Config.ALTURA_CELULA - 15))
                
            except Exception as e:
                print(f"  ERRO ao renderizar texto: {e}")
                
        except Exception as e:
            print(f"  ERRO ao processar aula: {e}")
            import traceback
            traceback.print_exc()
    
    pygame.display.flip()

def _processar_eventos() -> bool:
    """
    Processa eventos de entrada do Pygame e gerencia a interação do usuário.
    
    Esta função é responsável por:
    1. Capturar eventos do teclado e mouse
    2. Processar comandos de saída (ESC ou fechar janela)
    3. Manter a responsividade da interface
    
    Returns:
        bool: 
            - False se o usuário solicitou para sair (ESC ou fechar janela)
            - True para continuar a execução normal
            
    Notas:
        - Esta função é usada internamente pelo loop principal de visualização
        - Qualquer exceção durante o processamento de eventos é capturada e registrada
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
    return True


# Variáveis globais para manter o estado da visualização
fig = None
ax_grade = None
ax_evolucao = None
ax_distribuicao = None

def inicializar_visualizacao():
    """Inicializa a janela de visualização com matplotlib."""
    global fig, ax_grade, ax_evolucao, ax_distribuicao, canvas
    
    # Fecha a figura anterior se existir
    if fig is not None:
        plt.close(fig)
    
    # Cria uma nova figura com dois subplots lado a lado
    fig = plt.figure(figsize=(16, 8))
    gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])
    
    # Cria os subplots
    ax_grade = plt.subplot(gs[:, 0])  # Grade ocupa a coluna inteira à esquerda
    ax_evolucao = plt.subplot(gs[0, 1])  # Gráfico de evolução no canto superior direito
    ax_distribuicao = plt.subplot(gs[1, 1])  # Gráfico de distribuição no canto inferior direito
    
    # Configurações iniciais dos eixos
    ax_grade.set_title('Grade Horária')
    ax_evolucao.set_title('Evolução do Fitness')
    ax_distribuicao.set_title('Distribuição de Fitness')
    
    # Ajusta o layout
    plt.tight_layout()
    plt.ion()  # Modo interativo
    plt.show(block=False)

def visualizar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float, 
                    populacao: List[Dict[str, Any]] = None, 
                    calcular_fitness_func = None,
                    fechar_ao_terminar: bool = False,
                    mostrar_evolucao: bool = True) -> bool:
    """
    Exibe a grade horária e os gráficos de evolução usando matplotlib.
    
    Args:
        grade: Lista de dicionários representando a grade horária.
        geracao: Número da geração atual.
        fitness: Valor de fitness da melhor solução.
        populacao: Lista da população atual (opcional).
        calcular_fitness_func: Função para calcular o fitness (opcional).
        fechar_ao_terminar: Se True, fecha a janela após exibir.
        mostrar_evolucao: Se True, mostra os gráficos de evolução.
        
    Returns:
        True se a visualização deve continuar, False caso contrário.
    """
    """
    Exibe a grade horária e os gráficos de evolução em uma única janela.
    
    Args:
        grade: Lista de dicionários contendo as informações das aulas.
        geracao: Número da geração atual do algoritmo genético.
        fitness: Valor de fitness da grade atual.
        populacao: Lista de dicionários contendo os indivíduos da população atual (opcional).
        calcular_fitness_func: Função para calcular o fitness de um indivíduo.
        fechar_ao_terminar: Se True, fecha a janela automaticamente após um curto período.
        
    Returns:
        bool: True se a janela deve permanecer aberta, False se o usuário solicitou para sair.
    """
    global janela_grade, pygame_initialized, fonte_pequena, fonte_media, fonte_grande, estatisticas
    
    # Inicializa o Pygame se ainda não estiver inicializado
    if not pygame_initialized:
        if not inicializar_pygame():
            print("Erro: Não foi possível inicializar o Pygame.")
            return False
    
    # Garante que a grade seja uma lista de dicionários
    if not isinstance(grade, list):
        print(f"Erro: A grade deve ser uma lista, mas recebido: {type(grade)}")
        return False
        
    # Verifica se a grade tem itens e se são dicionários
    if grade and not all(isinstance(item, dict) for item in grade):
        print("Erro: A grade deve conter apenas dicionários.")
        return False
    
    # Atualiza as estatísticas da população se fornecida
    if populacao is not None and calcular_fitness_func is not None:
        try:
            estatisticas.adicionar_geracao(geracao, populacao, calcular_fitness_func)
            
            # Armazena a população atual para uso nos gráficos
            if not hasattr(estatisticas, 'ultima_populacao'):
                estatisticas.ultima_populacao = []
            estatisticas.ultima_populacao = list(populacao)
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")
            import traceback
            traceback.print_exc()
    
    # Configura o título da janela
    pygame.display.set_caption(f"Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}")
    
    # Limpa a tela com fundo branco
    janela_grade.fill(Config.BRANCO)
    
    # Calcula as dimensões para os frames
    if mostrar_evolucao:
        # Se mostrando evolução, divide a tela em duas partes iguais
        largura_evolucao = Config.LARGURA_JANELA // 2 - Config.MARGEM // 2
        largura_grade = Config.LARGURA_JANELA // 2 - Config.MARGEM // 2
        x_grade = largura_evolucao + Config.MARGEM
        
        # Frame esquerdo: Gráficos de evolução
        pygame.draw.rect(janela_grade, Config.BRANCO, (0, 0, largura_evolucao, Config.ALTURA_JANELA))
        
        # Altura para cada gráfico (metade da altura da janela, com margem)
        altura_grafico = (Config.ALTURA_JANELA - Config.MARGEM * 3) // 2
        
        # Gráfico de evolução (parte superior esquerda)
        desenhar_grafico_evolucao(janela_grade, 
                                 0, 
                                 Config.MARGEM, 
                                 largura_evolucao, 
                                 altura_grafico)
        
        # Gráfico de distribuição (parte inferior esquerda)
        desenhar_grafico_distribuicao(janela_grade,
                                     0,
                                     altura_grafico + Config.MARGEM * 2,
                                     largura_evolucao,
                                     altura_grafico)
        
        # Desenha a grade no frame da direita
        pygame.draw.rect(janela_grade, Config.BRANCO, (x_grade, 0, largura_grade, Config.ALTURA_JANELA))
        desenhar_grade(grade, geracao, fitness, x_grade, 0, largura_grade, Config.ALTURA_JANELA)
        
        # Desenha uma linha divisória entre os frames
        pygame.draw.line(janela_grade, Config.CINZA, 
                        (largura_evolucao + Config.MARGEM // 2, 0), 
                        (largura_evolucao + Config.MARGEM // 2, Config.ALTURA_JANELA), 2)
    else:
        # Se não for mostrar evolução, usa toda a largura para a grade
        desenhar_grade(grade, geracao, fitness, 0, 0, Config.LARGURA_JANELA, Config.ALTURA_JANELA)
    
    # Atualiza a tela
    pygame.display.flip()
    
    # Processa eventos para manter a janela responsiva
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            finalizar_visualizacao()
            return False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                finalizar_visualizacao()
                return False
            elif evento.key == pygame.K_s:  # Tecla 's' para salvar a imagem
                try:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    caminho = f"grade_geracao_{geracao}_{timestamp}.png"
                    salvar_imagem_grade(grade, caminho, geracao, fitness)
                    print(f"Imagem salva como: {os.path.abspath(caminho)}")
                except Exception as e:
                    print(f"Erro ao salvar a imagem: {e}")
    
    # Se não for para fechar automaticamente, entra em um loop de eventos
    if not fechar_ao_terminar:
        executando = True
        relogio = pygame.time.Clock()
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                        executando = False
                    elif evento.key == pygame.K_s:  # Tecla 's' para salvar a imagem
                        try:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            caminho = f"grade_geracao_{geracao}_{timestamp}.png"
                            salvar_imagem_grade(grade, caminho, geracao, fitness)
                            print(f"Imagem salva como: {os.path.abspath(caminho)}")
                        except Exception as e:
                            print(f"Erro ao salvar a imagem: {e}")
            
            relogio.tick(30)  # Limita a 30 FPS
            
    return True

def salvar_imagem_grade(grade: List[Dict[str, Any]], caminho: str, geracao: int, fitness: float) -> str:
    """
    Salva a grade horária como uma imagem em um arquivo.
    
    Esta função renderiza a grade horária em uma superfície Pygame e a salva como uma
    imagem no sistema de arquivos. O formato da imagem é determinado pela extensão
    do arquivo (suporta .png, .jpg, .jpeg, .bmp, .tga). Se nenhuma extensão for
    fornecida, será usado .png por padrão.
    
    Args:
        grade: Lista de dicionários contendo as informações das aulas, onde cada
            dicionário deve conter as chaves: 'disciplina', 'sala', 'professor',
            'dia' e 'horario'.
        caminho: Caminho onde a imagem será salva. Diretórios serão criados
            automaticamente se não existirem.
        geracao: Número da geração atual do algoritmo genético.
        fitness: Valor de fitness da grade atual (0.0 a 1.0).
        
    Returns:
        str: Caminho completo do arquivo salvo.
        
    Raises:
        ValueError: Se o formato do arquivo não for suportado.
        pygame.error: Se ocorrer um erro ao salvar a imagem.
        Exception: Para outros erros inesperados.
    """
    global janela_grade
    
    try:
        # Verifica se o Pygame foi inicializado
        if not pygame_initialized:
            if not inicializar_pygame():
                raise Exception("Não foi possível inicializar o Pygame")
        
        # Cria uma superfície temporária para renderizar a grade
        largura_grade = Config.LARGURA_JANELA // 2 - Config.MARGEM // 2
        superficie = pygame.Surface((largura_grade, Config.ALTURA_JANELA))
        superficie.fill(Config.BRANCO)
        
        # Renderiza a grade na superfície temporária
        janela_grade_original = janela_grade
        janela_grade = superficie
        desenhar_grade(grade, geracao, fitness, 0, 0, largura_grade, Config.ALTURA_JANELA)
        janela_grade = janela_grade_original
        
        # Garante que o diretório de destino existe
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        
        # Determina o formato com base na extensão do arquivo
        _, extensao = os.path.splitext(caminho)
        if not extensao:
            caminho += ".png"
            extensao = ".png"
        
        extensao = extensao.lower()
        formatos_suportados = {
            '.png': 'PNG',
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.bmp': 'BMP',
            '.tga': 'TGA'
        }
        
        if extensao not in formatos_suportados:
            raise ValueError(f"Formato de arquivo não suportado: {extensao}. Use: {', '.join(formatos_suportados.keys())}")
        
        # Salva a superfície como imagem
        pygame.image.save(superficie, caminho)
        
        # Retorna o caminho absoluto do arquivo salvo
        return os.path.abspath(caminho)
        
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        raise

def desenhar_grafico_evolucao(surface: pygame.Surface, x: int, y: int, largura: int, altura: int) -> None:
    """
    Desenha um gráfico mostrando a evolução do fitness ao longo das gerações.
    
    Args:
        surface: Superfície onde o gráfico será desenhado.
        x: Posição X do canto superior esquerdo do gráfico.
        y: Posição Y do canto superior esquerdo do gráfico.
        largura: Largura do gráfico.
        altura: Altura do gráfico.
    """
    global janela_grade, fonte_pequena, fonte_media, estatisticas
    
    # Verifica se temos dados suficientes
    if not hasattr(estatisticas, 'geracoes') or not hasattr(estatisticas, 'melhores_fitness') or not estatisticas.geracoes or not estatisticas.melhores_fitness:
        return
    
    # Verifica se as fontes foram carregadas
    if fonte_pequena is None or fonte_media is None or janela_grade is None:
        return
    
    # Configurações do gráfico
    margem = 50
    largura = Config.LARGURA_JANELA // 2 - 2 * margem
    altura = Config.ALTURA_GRAFICO - 2 * margem
    
    # Desenha o fundo do gráfico
    pygame.draw.rect(surface, Config.BRANCO, (0, 0, Config.LARGURA_JANELA // 2, Config.ALTURA_GRAFICO))
    
    # Título do gráfico
    texto_titulo = fonte_media.render("Evolução do Fitness por Geração", True, Config.PRETO)
    surface.blit(texto_titulo, (x + (largura - texto_titulo.get_width()) // 2, y + 10))
    
    # Encontra os valores máximos e mínimos para escalar o gráfico
    max_fitness = max(estatisticas.melhores_fitness)
    min_fitness = min(estatisticas.piores_fitness) if estatisticas.piores_fitness else 0
    
    # Garante que haja uma diferença mínima para evitar divisão por zero
    if max_fitness == min_fitness:
        max_fitness += 1
        min_fitness = max(0, min_fitness - 1)
    
    # Desenha os eixos
    pygame.draw.line(surface, Config.PRETO, 
                    (margem, margem + altura), 
                    (margem + largura, margem + altura), 2)  # Eixo X
    
    pygame.draw.line(surface, Config.PRETO, 
                    (margem, margem), 
                    (margem, margem + altura), 2)  # Eixo Y
    
    # Desenha as linhas de grade e os rótulos do eixo Y
    for i in range(6):
        y = margem + altura - (i * altura // 5)
        valor = min_fitness + (i * (max_fitness - min_fitness) / 5)
        
        # Linha de grade
        pygame.draw.line(surface, Config.CINZA, 
                        (margem, y), 
                        (margem + largura, y), 1)
        
        # Rótulo do eixo Y
        texto = fonte_pequena.render(f"{valor:.1f}", True, Config.PRETO)
        surface.blit(texto, (margem - 35, y - 8))
    
    # Desenha as linhas do gráfico se houver dados suficientes
    if len(estatisticas.geracoes) > 1:
        # Melhor fitness
        pontos_melhor = []
        for i, (gen, fit) in enumerate(zip(estatisticas.geracoes, estatisticas.melhores_fitness)):
            x = margem + (i * largura / (len(estatisticas.geracoes) - 1))
            y = margem + altura - ((fit - min_fitness) / (max_fitness - min_fitness) * altura)
            pontos_melhor.append((x, y))
        
        if len(pontos_melhor) > 1:
            pygame.draw.lines(surface, Config.VERDE_ESCURO, False, pontos_melhor, 2)
        
        # Média de fitness (se disponível)
        if estatisticas.medias_fitness and len(estatisticas.medias_fitness) == len(estatisticas.geracoes):
            pontos_media = []
            for i, (gen, fit) in enumerate(zip(estatisticas.geracoes, estatisticas.medias_fitness)):
                x = margem + (i * largura / (len(estatisticas.geracoes) - 1))
                y = margem + altura - ((fit - min_fitness) / (max_fitness - min_fitness) * altura)
                pontos_media.append((x, y))
            
            if len(pontos_media) > 1:
                pygame.draw.lines(surface, Config.AZUL_ESCURO, False, pontos_media, 1)
        
        # Pior fitness (se disponível)
        if estatisticas.piores_fitness and len(estatisticas.piores_fitness) == len(estatisticas.geracoes):
            pontos_pior = []
            for i, (gen, fit) in enumerate(zip(estatisticas.geracoes, estatisticas.piores_fitness)):
                x = margem + (i * largura / (len(estatisticas.geracoes) - 1))
                y = margem + altura - ((fit - min_fitness) / (max_fitness - min_fitness) * altura)
                pontos_pior.append((x, y))
            
            if len(pontos_pior) > 1:
                pygame.draw.lines(surface, Config.VERMELHO_ESCURO, False, pontos_pior, 1)
    
    # Rótulos do eixo X
    if estatisticas.geracoes:
        # Rótulos do eixo X
        if hasattr(estatisticas, 'geracoes') and estatisticas.geracoes:
            texto_inicio = fonte_pequena.render(str(estatisticas.geracoes[0]), True, Config.PRETO)
            surface.blit(texto_inicio, (margem - 10, margem + altura + 5))
            
            # Última geração
            texto_fim = fonte_pequena.render(str(estatisticas.geracoes[-1]), True, Config.PRETO)
            surface.blit(texto_fim, (margem + largura - 15, margem + altura + 5))
    
    # Legenda
    if hasattr(estatisticas, 'melhores_fitness') and estatisticas.melhores_fitness:
        legenda_y = margem + 10
        legenda_x = largura - 150
        
        # Melhor fitness
        pygame.draw.line(surface, Config.VERDE_ESCURO, 
                        (legenda_x, legenda_y + 5), 
                        (legenda_x + 30, legenda_y + 5), 2)
        texto_legenda = fonte_pequena.render("Melhor", True, Config.PRETO)
        surface.blit(texto_legenda, (x + largura - 150, y + 30))
        # Valor numérico do melhor fitness atual
        if hasattr(estatisticas, 'melhores_fitness') and estatisticas.melhores_fitness:
                texto_valor = fonte_media.render(f"Melhor: {estatisticas.melhores_fitness[-1]:.2f}", True, Config.VERDE_ESCURO)
                surface.blit(texto_valor, (x + 20, y + 20))

def desenhar_grafico_distribuicao(surface: pygame.Surface, x_inicio: int, y_inicio: int, largura: int, altura: int) -> None:
    """
    Desenha um gráfico de distribuição de fitness na população atual.
    
    Args:
        surface: Superfície onde o gráfico será desenhado
        x_inicio: Posição X do canto superior esquerdo do gráfico
        y_inicio: Posição Y do canto superior esquerdo do gráfico
        largura: Largura do gráfico
        altura: Altura do gráfico
    """
    global fonte_pequena, fonte_media, estatisticas
    
    # Verifica se temos população para exibir
    if not hasattr(estatisticas, 'ultima_populacao') or not estatisticas.ultima_populacao:
        # Desenha uma mensagem informativa
        texto = fonte_media.render("Sem dados de população", True, Config.VERMELHO)
        surface.blit(texto, (x_inicio + 20, y_inicio + 20))
        return
    
    try:
        # Configurações do gráfico
        margem = 50
        num_barras = 10
        
        # Coleta os valores de fitness da população de forma segura
        fitness_values = []
        for individuo in estatisticas.ultima_populacao:
            try:
                # Tenta obter o fitness de diferentes maneiras
                if isinstance(individuo, dict):
                    if 'fitness' in individuo:
                        fitness_values.append(float(individuo['fitness']))
                    elif hasattr(individuo, 'fitness'):
                        fitness_values.append(float(individuo.fitness))
                elif hasattr(individuo, 'get'):
                    fitness = individuo.get('fitness')
                    if fitness is not None:
                        fitness_values.append(float(fitness))
                elif hasattr(individuo, 'fitness'):
                    fitness_values.append(float(individuo.fitness))
            except (TypeError, ValueError) as e:
                print(f"Aviso: Não foi possível obter o fitness do indivíduo: {e}")
                continue
        
        if not fitness_values:
            # Se não encontrou valores de fitness válidos
            texto = fonte_media.render("Sem dados de fitness válidos", True, Config.VERMELHO)
            surface.blit(texto, (x_inicio + 20, y_inicio + 20))
            return
        
        # Calcula os intervalos das barras
        min_fitness = min(fitness_values)
        max_fitness = max(fitness_values)
        if max_fitness == min_fitness:
            max_fitness = min_fitness + 1  # Evita divisão por zero
        
        # Calcula a largura de cada barra
        largura_barra = (largura - 2 * margem) / num_barras
        
        # Desenha o fundo do gráfico
        pygame.draw.rect(surface, Config.BRANCO, (x_inicio, y_inicio, largura, altura))
        pygame.draw.rect(surface, Config.PRETO, (x_inicio, y_inicio, largura, altura), 2)
        
        # Desenha as barras
        for i in range(num_barras):
            # Calcula o intervalo de valores para esta barra
            valor_min = min_fitness + (i * (max_fitness - min_fitness) / num_barras)
            valor_max = min_fitness + ((i + 1) * (max_fitness - min_fitness) / num_barras)
            
            # Conta quantos valores estão neste intervalo
            count = sum(1 for f in fitness_values if valor_min <= f < valor_max)
            if i == num_barras - 1:  # Inclui o valor máximo na última barra
                count = sum(1 for f in fitness_values if valor_min <= f <= valor_max)
            
            # Calcula a altura da barra
            max_count = max(1, len(fitness_values) // 2)  # Evita divisão por zero
            altura_barra = (count / max_count) * (altura - 2 * margem) if max_count > 0 else 0
            
            # Posiciona a barra
            x = x_inicio + margem + (i * largura_barra)
            y = y_inicio + altura - margem - altura_barra
            
            # Cor gradiente baseada na altura da barra
            cor_azul = max(100, min(255, 100 + int(155 * (count / max_count))))
            cor = (100, 100, cor_azul)
            
            # Desenha a barra
            pygame.draw.rect(surface, cor, (x, y, largura_barra - 2, altura_barra))
            pygame.draw.rect(surface, Config.PRETO, (x, y, largura_barra - 2, altura_barra), 1)
            
            # Adiciona o valor da contagem em cima da barra se houver espaço
            if altura_barra > 15 and count > 0:
                texto = fonte_pequena.render(str(count), True, Config.PRETO)
                surface.blit(texto, (x + (largura_barra - texto.get_width()) // 2, y - 15))
        
        # Desenha os eixos
        pygame.draw.line(surface, Config.PRETO, 
                        (x_inicio + margem, y_inicio + altura - margem), 
                        (x_inicio + largura - margem, y_inicio + altura - margem), 2)  # Eixo X
        pygame.draw.line(surface, Config.PRETO, 
                        (x_inicio + margem, y_inicio + altura - margem), 
                        (x_inicio + margem, y_inicio + margem), 2)  # Eixo Y
        
        # Rótulos dos eixos
        texto_x = fonte_pequena.render("Fitness", True, Config.PRETO)
        texto_y = fonte_pequena.render("Frequência", True, Config.PRETO)
        surface.blit(texto_x, (x_inicio + largura // 2 - texto_x.get_width() // 2, 
                              y_inicio + altura - 20))
        
        # Rótulos do eixo Y (frequência)
        max_count = max(1, max((sum(1 for f in fitness_values if 
                                  min_fitness + (i * (max_fitness - min_fitness) / num_barras) <= f < 
                                  min_fitness + ((i + 1) * (max_fitness - min_fitness) / num_barras)) 
                              for i in range(num_barras)), default=0))
        
        for i in range(0, 6):  # 5 marcas no eixo Y
            valor = (max_count * i) // 5
            y = y_inicio + altura - margem - ((altura - 2 * margem) * i) // 5
            texto = fonte_pequena.render(str(valor), True, Config.PRETO)
            surface.blit(texto, (x_inicio + margem - texto.get_width() - 5, y - 6))
            pygame.draw.line(surface, Config.CINZA, 
                           (x_inicio + margem - 5, y), 
                           (x_inicio + margem, y), 1)
        
        # Rótulos do eixo X (valores de fitness)
        for i in range(0, 6):
            x = x_inicio + margem + (i * (largura - 2 * margem) // 5)
            valor = min_fitness + (i * (max_fitness - min_fitness) / 5)
            texto = fonte_pequena.render(f"{valor:.1f}", True, Config.PRETO)
            surface.blit(texto, (x - 20, y_inicio + altura - margem + 5))
        
        # Título do gráfico
        titulo = "Distribuição de Fitness"
        texto_titulo = fonte_media.render(titulo, True, Config.PRETO)
        surface.blit(texto_titulo, (x_inicio + (largura - texto_titulo.get_width()) // 2, 
                                   y_inicio + 10))
    
    except Exception as e:
        print(f"Erro ao desenhar gráfico de distribuição: {e}")
        import traceback
        traceback.print_exc()
        
        # Desenha mensagem de erro na superfície
        texto_erro = fonte_media.render("Erro ao gerar gráfico", True, Config.VERMELHO)
        surface.blit(texto_erro, (x_inicio + 20, y_inicio + 20))


def finalizar_visualizacao() -> None:
    """
    Finaliza o Pygame e libera todos os recursos associados.
    
    Esta função deve ser chamada quando a visualização não for mais necessária
    para garantir a liberação adequada dos recursos do sistema. Ela:
    
    1. Encerra o Pygame se estiver inicializado
    2. Limpa as referências a recursos gráficos
    3. Reseta as variáveis de estado do módulo
    
    Nota: Esta função é chamada automaticamente por `visualizar_grade` quando
    o usuário fecha a janela, mas pode ser chamada manualmente se necessário.
    """
    global pygame_initialized, janela_grade, janela_graficos, fonte_pequena, fonte_media, fonte_grande

    try:
        # Limpa as referências às fontes
        fonte_pequena = None
        fonte_media = None
        fonte_grande = None
        
        # Fecha as janelas se existirem
        if pygame_initialized:
            if janela_grade is not None:
                pygame.display.quit()
                janela_grade = None
            
            if janela_graficos is not None:
                pygame.display.quit()
                janela_graficos = None
        
        # Encerra o Pygame se estiver inicializado
        if pygame_initialized:
            pygame.quit()
            pygame_initialized = False
            
    except Exception as e:
        print(f"Erro ao finalizar a visualização: {e}")
