"""
Módulo principal do Algoritmo Genético para otimização de grade horária.

Este módulo contém as funções e constantes essenciais para a execução
do algoritmo genético de alocação de horários.
"""
import random
from typing import List, Dict, Any

# ================== DADOS DO PROBLEMA ==================
DISCIPLINAS = [
    {"nome": "Cálculo I", "tipo": "teorica", "professor": "Ana", "sala_requerida": "Sala 101", "preferencia": "manha"},
    {"nome": "Algoritmos e Programação", "tipo": "laboratorio", "professor": "Alice", "sala_requerida": "Lab. Software", "preferencia": "tarde"},
    {"nome": "Circuitos Digitais", "tipo": "laboratorio", "professor": "Carlos", "sala_requerida": "Lab. Hardware", "preferencia": "tarde"},
    {"nome": "Inteligência Artificial", "tipo": "teorica", "professor": "Bruno", "sala_requerida": "Sala 102", "preferencia": "qualquer"},
    {"nome": "Sistemas Operacionais", "tipo": "laboratorio", "professor": "Bruno", "sala_requerida": "Lab. Software", "preferencia": "manha"},
]

SALAS = ["Sala 101", "Sala 102", "Lab. Software", "Lab. Hardware"]
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
# Formatos de horário atualizados para corresponder exatamente ao formato esperado na visualização
HORARIOS_MANHA = ["08:00-10:00", "10:00-12:00"]
HORARIOS_TARDE = ["13:30-15:30", "15:30-17:30"]

# ================== FUNÇÕES DO AG ==================
def gerar_individuo() -> List[Dict[str, Any]]:
    """
    Gera um indivíduo (solução candidata) aleatório para o problema de alocação.
    
    Returns:
        List[Dict[str, Any]]: Lista de dicionários, onde cada dicionário representa uma aula 
        com atributos como disciplina, professor, sala, dia, horário, etc.
    """
    individuo = []
    for disciplina in DISCIPLINAS:
        # Escolhe horário baseado na preferência
        if disciplina["preferencia"] == "manha":
            horario = random.choice(HORARIOS_MANHA)
        elif disciplina["preferencia"] == "tarde":
            horario = random.choice(HORARIOS_TARDE)
        else:
            horario = random.choice(HORARIOS_MANHA + HORARIOS_TARDE)
        
        # Garante que o horário está no formato correto
        horario = horario.strip()
        
        aula = {
            "disciplina": disciplina["nome"],
            "professor": disciplina["professor"],
            "sala": disciplina["sala_requerida"],
            "dia": random.choice(DIAS),
            "horario": horario,
            "tipo": disciplina["tipo"],
            "preferencia": disciplina["preferencia"]
        }
        individuo.append(aula)
    return individuo

def calcular_fitness(individuo: List[Dict[str, Any]]) -> int:
    """
    Avalia a qualidade de um horário atribuindo pontuações com base em restrições.
    
    Args:
        individuo: Lista de aulas representando um horário candidato.
        
    Returns:
        int: Pontuação do indivíduo. Quanto maior a pontuação, melhor a solução.
        
    Pontuação:
        - Inicia com 1000 pontos
        - -200 pontos por conflito de professor
        - -200 pontos por conflito de sala
        - -300 pontos por sala incorreta para laboratórios
        - -50 pontos por desrespeito à preferência de horário
        - -150 pontos por ter duas disciplinas no mesmo horário e dia (mesmo em salas diferentes)
    """
    pontos = 1000
    # Verifica conflitos
    for i, aula1 in enumerate(individuo):
        for aula2 in individuo[i+1:]:
            # Conflito de professor
            if (aula1["dia"] == aula2["dia"] and 
                aula1["horario"] == aula2["horario"] and 
                aula1["professor"] == aula2["professor"]):
                pontos -= 200
            # Conflito de sala
            if (aula1["dia"] == aula2["dia"] and 
                aula1["horario"] == aula2["horario"] and 
                aula1["sala"] == aula2["sala"]):
                pontos -= 200
            # Conflito de horário (mesmo dia e horário, mesmo em salas diferentes)
            if (aula1["dia"] == aula2["dia"] and 
                aula1["horario"] == aula2["horario"]):
                pontos -= 150
        # Verifica se a sala está correta para laboratórios
        if (aula1["tipo"] == "laboratorio" and 
            aula1["sala"] != DISCIPLINAS[i]["sala_requerida"]):
            pontos -= 300
        # Verifica preferência de horário
        if ((aula1["preferencia"] == "manha" and aula1["horario"] not in HORARIOS_MANHA) or 
            (aula1["preferencia"] == "tarde" and aula1["horario"] not in HORARIOS_TARDE)):
            pontos -= 50
    return pontos

def crossover(pai1: List[Dict[str, Any]], pai2: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Realiza o cruzamento (crossover) entre dois indivíduos para gerar um filho.
    
    Args:
        pai1: Primeiro indivíduo pai.
        pai2: Segundo indivíduo pai.
        
    Returns:
        Novo indivíduo gerado a partir do cruzamento dos pais.
        
    Nota:
        Utiliza um ponto de corte aleatório para combinar partes de cada pai.
    """
    ponto_corte = random.randint(1, len(DISCIPLINAS)-1)
    filho = pai1[:ponto_corte] + pai2[ponto_corte:]
    return filho

def mutacao(individuo: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Aplica mutação em um indivíduo para introduzir diversidade genética.
    
    Args:
        individuo: Indivíduo que sofrerá mutação.
        
    Returns:
        Indivíduo com mutação aplicada.
        
    A mutação consiste em alterar aleatoriamente o dia e horário de uma aula.
    Garante que apenas horários válidos sejam usados.
    """
    if not individuo:
        return individuo
        
    # Cria uma cópia para não modificar o original diretamente
    novo_individuo = [aula.copy() for aula in individuo]
    
    # Seleciona uma aula aleatória para mutação
    aula_mutada = random.randint(0, len(novo_individuo)-1)
    
    # Escolhe um novo dia e horário válidos
    novo_dia = random.choice(DIAS)
    
    # Escolhe o horário baseado na preferência da disciplina
    disciplina = novo_individuo[aula_mutada]
    if disciplina["preferencia"] == "manha":
        novo_horario = random.choice(HORARIOS_MANHA)
    elif disciplina["preferencia"] == "tarde":
        novo_horario = random.choice(HORARIOS_TARDE)
    else:
        novo_horario = random.choice(HORARIOS_MANHA + HORARIOS_TARDE)
    
    # Garante que o horário está no formato correto
    novo_horario = novo_horario.strip()
    
    # Aplica as mutações
    novo_individuo[aula_mutada]["dia"] = novo_dia
    novo_individuo[aula_mutada]["horario"] = novo_horario
    
    return novo_individuo


def algoritmo_genetico(tamanho_populacao=100, geracoes=200, callback_visualizacao=None):
    """
    Executa o algoritmo genético para otimização da grade horária.
    
    Args:
        tamanho_populacao: Número de indivíduos na população.
        geracoes: Número de gerações para executar.
        callback_visualizacao: Função de callback para visualização em tempo real.
            Recebe (melhor_individuo, geracao_atual, melhor_fitness) como argumentos.
        
    Returns:
        Melhor indivíduo encontrado.
    """
    historico_fitness = []
    melhor_fitness_por_geracao = []
    
    # Gera população inicial
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    melhor_global = None
    melhor_fitness_global = -1
    
    for geracao in range(geracoes):
        # Avalia a população
        fitness_populacao = [calcular_fitness(ind) for ind in populacao]
        historico_fitness.extend(fitness_populacao)
        
        # Ordena a população pelo fitness (maior primeiro)
        populacao = [ind for _, ind in sorted(zip(fitness_populacao, populacao), key=lambda x: -x[0])]
        
        # Armazena o melhor fitness da geração
        melhor_fitness = max(fitness_populacao)
        melhor_individuo = populacao[0]
        
        # Atualiza o melhor global
        if melhor_fitness > melhor_fitness_global:
            melhor_global = melhor_individuo
            melhor_fitness_global = melhor_fitness
        
        melhor_fitness_por_geracao.append(melhor_fitness)
        
        # Chama o callback de visualização, se fornecido
        if callback_visualizacao and geracao % 5 == 0:  # Atualiza a cada 5 gerações
            try:
                callback_visualizacao(melhor_global, geracao, melhor_fitness_global)
            except Exception as e:
                print(f"Erro na visualização: {e}")
        
        # Seleciona os melhores (top 20%)
        melhores = populacao[:max(2, tamanho_populacao//5)]  # Garante pelo menos 2 indivíduos
        
        # Nova geração (crossover + mutação)
        nova_populacao = melhores.copy()  # Mantém os melhores (elitismo)
        
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.choices(melhores, k=2)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:  # 10% de chance de mutação
                filho = mutacao(filho)
            nova_populacao.append(filho)
            
        populacao = nova_populacao
        
        # Exibe progresso a cada 20 gerações
        if geracao % 20 == 0:
            print(f"Geração {geracao}: Melhor fitness = {melhor_fitness_global}")
        
        # Chama o callback de visualização, se fornecido
        if callback_visualizacao is not None:
            try:
                callback_visualizacao(melhor_global, geracao, melhor_fitness_global, populacao)
            except Exception as e:
                print(f"Erro na visualização: {e}")
    
    # Última atualização da visualização
    if callback_visualizacao is not None:
        try:
            callback_visualizacao(melhor_global, geracoes-1, melhor_fitness_global, populacao)
        except Exception as e:
            print(f"Erro na visualização final: {e}")
    
    return melhor_global