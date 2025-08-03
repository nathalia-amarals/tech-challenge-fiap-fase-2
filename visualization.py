"""
Módulo de visualização para o algoritmo genético de grade horária.

Este módulo fornece funções para visualização interativa da grade horária usando Pygame,
incluindo exibição em tempo real, salvamento de imagens e controle de visualização.
"""
import os
import sys
import pygame
import pygame.freetype
from typing import List, Dict, Any, Optional, Final

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
    LARGURA_JANELA: Final[int] = 1200
    LARGURA_INFO: Final[int] = 200
    ALTURA_JANELA: Final[int] = 700
    MARGEM: Final[int] = 20
    LARGURA_CELULA: Final[int] = 150
    ALTURA_CABECALHO: Final[int] = 40
    ALTURA_CELULA: Final[int] = 80
    FPS: Final[int] = 30

    # Dias da semana e horários
    DIAS: Final[list[str]] = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    HORARIOS: Final[list[str]] = ['08:00-10:00', '10:00-12:00', '13:30-15:30', '15:30-17:30']

# Variáveis de estado do módulo
pygame_initialized: bool = False
janela: Optional[pygame.Surface] = None
fonte_pequena: Optional[pygame.freetype.Font] = None
fonte_media: Optional[pygame.freetype.Font] = None
fonte_grande: Optional[pygame.freetype.Font] = None

def inicializar_pygame() -> bool:
    """
    Inicializa o Pygame e configura o ambiente de renderização.
    
    Esta função é responsável por:
    1. Inicializar o Pygame e o módulo de fontes
    2. Criar a janela de exibição se não existir
    3. Carregar e configurar as fontes necessárias
    
    Returns:
        bool: True se a inicialização foi bem-sucedida, False caso contrário.
        
    Nota:
        Em caso de falha ao carregar as fontes especificadas, a função 
        fará fallback para a fonte padrão do sistema.
    """
    global pygame_initialized, fonte_pequena, fonte_media, fonte_grande, janela
    
    try:
        if not pygame_initialized:
            pygame.init()
            pygame.freetype.init()
            pygame_initialized = True
        
        # Configuração da janela se não existir
        if janela is None:
            # Configuração para janela visível
            os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
            janela = pygame.display.set_mode((Config.LARGURA_JANELA, Config.ALTURA_JANELA))
            pygame.display.set_caption("Grade Horária - Algoritmo Genético")
        
        # Carrega as fontes se ainda não foram carregadas
        if fonte_pequena is None:
            try:
                # Tenta carregar a fonte Arial primeiro
                fonte_pequena = pygame.freetype.SysFont('Arial', 10)
                fonte_media = pygame.freetype.SysFont('Arial', 14)
                fonte_grande = pygame.freetype.SysFont('Arial', 18, bold=True)
                
                # Testa se as fontes foram carregadas corretamente
                if not all([fonte_pequena, fonte_media, fonte_grande]):
                    raise Exception("Falha ao carregar fontes Arial")
                    
            except Exception as e:
                print(f"Aviso: {e}. Usando fonte padrão do sistema.")
                # Fallback para fonte padrão do sistema
                fonte_padrao = pygame.freetype.get_default_font()
                fonte_pequena = pygame.freetype.SysFont(fonte_padrao, 10)
                fonte_media = pygame.freetype.SysFont(fonte_padrao, 14)
                fonte_grande = pygame.freetype.SysFont(fonte_padrao, 18, bold=True)
        
        return True
        
    except Exception as e:
        print(f"Erro ao inicializar o Pygame: {e}")
        pygame_initialized = False
        return False

def desenhar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float) -> None:
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
        
    Notas:
        - A função espera que as variáveis globais do Pygame já tenham sido
          inicializadas pela função `inicializar_pygame()`.
        - A função exibe mensagens de depuração no console para ajudar a
          identificar problemas com os dados da grade.
        - As cores das células são determinadas pelo tipo de sala (laboratório ou não).
    """
    global janela, fonte_pequena, fonte_media, fonte_grande
    
    # Garante que o Pygame está inicializado
    if not pygame_initialized:
        inicializar_pygame()
    
    # Preenche o fundo
    janela.fill(Config.BRANCO)
    
    # Desenha o título
    titulo = f"Grade Horária - Geração {geracao} - Fitness: {fitness:.2f}"
    titulo_surface, _ = fonte_media.render(titulo, Config.PRETO)
    janela.blit(titulo_surface, (Config.MARGEM, 10))
    
    # Desenha os cabeçalhos dos dias
    for i, dia in enumerate(Config.DIAS):
        x = Config.MARGEM + 100 + i * Config.LARGURA_CELULA
        y = Config.MARGEM + 50
        
        # Desenha o retângulo do cabeçalho do dia
        pygame.draw.rect(janela, Config.CINZA_CLARO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CABECALHO))
        pygame.draw.rect(janela, Config.PRETO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CABECALHO), 1)
        
        # Renderiza e desenha o texto do dia
        dia_surface, _ = fonte_pequena.render(dia, Config.PRETO)
        janela.blit(dia_surface, (x + 5, y + 5))
    
    # Desenha os horários
    for i, horario in enumerate(Config.HORARIOS):
        y = Config.MARGEM + 50 + Config.ALTURA_CABECALHO + i * Config.ALTURA_CELULA
        
        # Desenha o horário na lateral
        horario_surface, _ = fonte_pequena.render(horario, Config.PRETO)
        janela.blit(horario_surface, (Config.MARGEM, y + 5))
        
        # Desenha as linhas horizontais
        pygame.draw.line(janela, Config.CINZA, (Config.MARGEM, y), (Config.LARGURA_JANELA - Config.MARGEM, y), 1)
    
    # Desenha as linhas verticais
    for i in range(len(Config.DIAS) + 1):
        x = Config.MARGEM + 100 + i * Config.LARGURA_CELULA
        y_inicio = Config.MARGEM + 50
        y_fim = y_inicio + Config.ALTURA_CABECALHO + len(Config.HORARIOS) * Config.ALTURA_CELULA
        pygame.draw.line(janela, Config.CINZA, (x, y_inicio), (x, y_fim), 1)
    
    # Log de depuração
    print("\n=== DADOS DA GRADE ===")
    print(f"Geração: {geracao}, Fitness: {fitness}")
    print("Aulas na grade:")
    for i, aula in enumerate(grade, 1):
        print(f"  {i}. {aula.get('disciplina', 'Sem disciplina')} - {aula.get('dia', 'Sem dia')} {aula.get('horario', 'Sem horário')} ({aula.get('sala', 'Sem sala')})")
    
    print(f"\nHorários esperados na visualização: {Config.HORARIOS}")
    print(f"Dias esperados na visualização: {Config.DIAS}")
    print("="*24 + "\n")
    
    # Desenha as aulas
    for aula in grade:
        try:
            dia = aula.get('dia')
            horario = aula.get('horario')
            
            # Verifica se o dia e o horário são válidos
            if dia not in Config.DIAS:
                print(f"  AVISO: Dia inválido: {dia}")
                continue
                
            if horario not in Config.HORARIOS:
                print(f"  AVISO: Horário inválido: {horario}")
                continue
            
            dia_idx = Config.DIAS.index(dia)
            horario_idx = Config.HORARIOS.index(horario)
            
            x = Config.MARGEM + 100 + dia_idx * Config.LARGURA_CELULA
            y = Config.MARGEM + 50 + Config.ALTURA_CABECALHO + horario_idx * Config.ALTURA_CELULA
            
            # Escolhe a cor com base no tipo de sala
            cor = Config.AZUL if 'Lab' in str(aula.get('sala', '')) else Config.VERDE
            
            # Desenha o retângulo da aula
            pygame.draw.rect(janela, cor, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA))
            pygame.draw.rect(janela, Config.PRETO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA), 1)
            
            # Adiciona o texto da disciplina
            disciplina = str(aula.get('disciplina', 'Sem disciplina'))
            sala = str(aula.get('sala', 'Sem sala'))
            professor = str(aula.get('professor', 'Sem professor'))
            
            # Log de depuração
            print(f"  Desenhando em: dia_idx={dia_idx}, horario_idx={horario_idx}, pos=({x}, {y})")
            
            # Renderiza e desenha o texto
            try:
                # Quebra o texto da disciplina em várias linhas se necessário
                partes_disciplina = [disciplina[i:i+15] for i in range(0, len(disciplina), 15)]
                for i, parte in enumerate(partes_disciplina[:2]):  # Máximo de 2 linhas
                    texto_surface, _ = fonte_pequena.render(parte, Config.PRETO)
                    janela.blit(texto_surface, (x + 5, y + 5 + i * 15))
                
                # Sala e professor em linhas separadas
                sala_surface, _ = fonte_pequena.render(f"Sala: {sala}", Config.PRETO)
                prof_surface, _ = fonte_pequena.render(f"Prof: {professor}", Config.PRETO)
                
                janela.blit(sala_surface, (x + 5, y + 35))
                janela.blit(prof_surface, (x + 5, y + 50))
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

def visualizar_grade(grade: List[Dict[str, Any]], geracao: int, fitness: float) -> None:
    """
    Exibe a grade horária em uma janela interativa.
    
    Esta função inicia o loop principal de visualização, processa eventos de entrada
    e mantém a grade atualizada até que o usuário feche a janela.
    
    Args:
        grade: Lista de dicionários contendo as informações das aulas.
        geracao: Número da geração atual do algoritmo genético.
        fitness: Valor de fitness da grade atual (0.0 a 1.0).
    """
    global janela
    
    if not inicializar_pygame() or janela is None:
        print("Erro: Não foi possível inicializar a visualização.")
        return
    
    try:
        pygame.display.set_caption(f"Grade Horária - Geração {geracao}")
        clock = pygame.time.Clock()
        executando = True
        
        while executando:
            # Processa eventos e verifica se deve continuar executando
            if not _processar_eventos():
                break
            
            # Desenha a grade completa
            desenhar_grade(grade, geracao, fitness)
            
            # Controla a taxa de quadros
            clock.tick(Config.FPS)
            
    except Exception as e:
        print(f"Erro durante a visualização: {e}")
        import traceback
        traceback.print_exc()
    finally:
        finalizar_visualizacao()

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
        str: Caminho absoluto para o arquivo de imagem salvo.
        
    Raises:
        pygame.error: Se ocorrer um erro ao salvar a imagem.
        OSError: Se não for possível criar os diretórios necessários.
        
    Exemplo:
        >>> salvar_imagem_grade(grade, 'resultados/grade_geracao_10.png', 10, 0.85)
        '/caminho/completo/resultados/grade_geracao_10.png'
    """
    global janela
    
    # Garante que o Pygame está inicializado
    inicializar_pygame()
    
    # Cria uma superfície temporária para desenhar
    superficie = pygame.Surface((Config.LARGURA_JANELA, Config.ALTURA_JANELA))
    
    # Desenha a grade na superfície
    superficie.fill(Config.BRANCO)
    
    # Desenha o cabeçalho
    fonte_grande.render_to(superficie, (Config.MARGEM, Config.MARGEM), 
                          f"Grade Horária - Geração {geracao}", Config.PRETO)
    
    # Desenha as informações à direita
    fonte_media.render_to(superficie, (Config.LARGURA_JANELA - Config.LARGURA_INFO + Config.MARGEM, Config.MARGEM),
                         f"Adequação: {fitness:.2f}", Config.PRETO)
    
    # Desenha os cabeçalhos dos dias
    for i, dia in enumerate(Config.DIAS):
        x = Config.MARGEM + i * Config.LARGURA_CELULA
        pygame.draw.rect(superficie, Config.CINZA, (x, Config.MARGEM + 50, Config.LARGURA_CELULA, Config.ALTURA_CABECALHO))
        fonte_media.render_to(superficie, (x + 10, Config.MARGEM + 65), dia, Config.PRETO)
    
    # Desenha os horários e células
    for i, horario in enumerate(Config.HORARIOS):
        y = Config.MARGEM + 50 + Config.ALTURA_CABECALHO + i * Config.ALTURA_CELULA
        
        # Desenha o horário
        pygame.draw.rect(superficie, Config.CINZA, (Config.MARGEM, y, 100, Config.ALTURA_CELULA))
        fonte_pequena.render_to(superficie, (Config.MARGEM + 5, y + 5), horario, Config.PRETO)
        
        # Desenha as células para cada dia
        for j in range(len(Config.DIAS)):
            x = Config.MARGEM + 100 + j * Config.LARGURA_CELULA
            pygame.draw.rect(superficie, Config.CINZA_CLARO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA), 1)
    
    # Preenche as células com as aulas
    for aula in grade:
        try:
            dia_idx = Config.DIAS.index(aula['dia'])
            horario_idx = Config.HORARIOS.index(aula['horario'])
            
            x = Config.MARGEM + 100 + dia_idx * Config.LARGURA_CELULA
            y = Config.MARGEM + 50 + Config.ALTURA_CABECALHO + horario_idx * Config.ALTURA_CELULA
            
            # Escolhe a cor com base no tipo de sala
            cor = Config.AZUL if 'Lab' in str(aula.get('sala', '')) else Config.VERDE
            
            # Desenha o retângulo da aula
            pygame.draw.rect(superficie, cor, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA))
            pygame.draw.rect(superficie, Config.PRETO, (x, y, Config.LARGURA_CELULA, Config.ALTURA_CELULA), 1)
            
            # Adiciona o texto da disciplina
            disciplina = str(aula.get('disciplina', 'Sem disciplina'))
            sala = str(aula.get('sala', 'Sem sala'))
            professor = str(aula.get('professor', 'Sem professor'))
            
            # Quebra o texto da disciplina em várias linhas se necessário
            partes_disciplina = [disciplina[i:i+15] for i in range(0, len(disciplina), 15)]
            for i, parte in enumerate(partes_disciplina[:2]):  # Máximo de 2 linhas
                texto_surface, _ = fonte_pequena.render(parte, Config.PRETO)
                superficie.blit(texto_surface, (x + 5, y + 5 + i * 15))
            
            # Sala e professor em linhas separadas
            sala_surface, _ = fonte_pequena.render(f"Sala: {sala}", Config.PRETO)
            prof_surface, _ = fonte_pequena.render(f"Prof: {professor}", Config.PRETO)
            
            superficie.blit(sala_surface, (x + 5, y + 35))
            superficie.blit(prof_surface, (x + 5, y + 50))
        except (ValueError, KeyError) as e:
            # Ignora erros de índice ou chave inválida
            continue
    
    # Garante que o diretório existe
    diretorio = os.path.dirname(os.path.abspath(caminho))
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
    
    # Adiciona extensão .png se não tiver
    if not caminho.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tga')):
        caminho += '.png'
    
    # Salva a imagem
    pygame.image.save(superficie, caminho)
    return os.path.abspath(caminho)

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
    global pygame_initialized, janela, fonte_pequena, fonte_media, fonte_grande

    try:
        # Só tenta finalizar se o Pygame estiver inicializado
        if pygame_initialized and 'pygame' in globals() and pygame.get_init():
            pygame.quit()
    except Exception as e:
        print(f"Aviso ao finalizar o Pygame: {e}")
    finally:
        # Garante que todas as referências sejam limpas
        janela = None
        fonte_pequena = None
        fonte_media = None
        fonte_grande = None
        pygame_initialized = False
