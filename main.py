"""
Sistema de Otimização de Grade Horária com Algoritmo Genético

Este módulo implementa a interface de linha de comando e visualização para
o algoritmo genético de alocação de horários acadêmicos.

Autor: Nathalia Amaral
Data: Agosto 2025
"""
import sys
import os
import pygame
import argparse
import time
import matplotlib.pyplot as plt
from pprint import pprint
import genetic_algorithm as ga
from visualization_clean import visualizar_grade, salvar_imagem_grade, finalizar_visualizacao

def acompanhar_evolucao(historico_fitness, melhor_fitness_por_geracao):
    """
    Gera gráficos mostrando a evolução do fitness ao longo das gerações.
    
    Args:
        historico_fitness: Lista com o fitness de todos os indivíduos.
        melhor_fitness_por_geracao: Lista com o melhor fitness de cada geração.
    """
    plt.figure(figsize=(12, 6))
    
    # Gráfico 1: Fitness de todos os indivíduos
    plt.subplot(1, 2, 1)
    plt.plot(historico_fitness, 'b-', alpha=0.3, linewidth=0.5)
    plt.title('Distribuição de Fitness')
    plt.xlabel('Avaliações')
    plt.ylabel('Fitness')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Gráfico 2: Evolução do melhor fitness
    plt.subplot(1, 2, 2)
    plt.plot(melhor_fitness_por_geracao, 'r-', linewidth=2, 
             marker='o', markersize=4, markevery=len(melhor_fitness_por_geracao)//10)
    plt.title('Evolução do Melhor Fitness')
    plt.xlabel('Geração')
    plt.ylabel('Melhor Fitness')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()


def executar_algoritmo_genetico(tamanho_populacao=50, geracoes=100, mostrar_visualizacao=False):
    """
    Executa o algoritmo genético e exibe os resultados.
    
    Args:
        tamanho_populacao: Número de indivíduos na população.
        geracoes: Número de gerações para executar.
        mostrar_visualizacao: Se True, mostra a visualização ao final.
        
    Returns:
        Melhor grade horária encontrada.
    """
    print("\nIniciando algoritmo genético...")
    print(f"Configuração: População={tamanho_populacao}, Gerações={geracoes}")
    
    # Inicializa o pygame se a visualização estiver ativada
    if mostrar_visualizacao:
        pygame.init()
    
    # Variáveis para armazenar a população atual
    populacao_atual = []
    
    # Callback para visualização em tempo real
    def callback_visualizacao(melhor_grade, geracao, fitness, populacao=None, finalizar=False):
        nonlocal populacao_atual
        if populacao is not None:
            populacao_atual = populacao
        
        # Se a visualização estiver ativada, mostra em tempo real
        if mostrar_visualizacao:
            try:
                # Atualiza a visualização
                continuar = visualizar_grade(
                    melhor_grade,
                    geracao,
                    fitness,
                    populacao=populacao_atual,
                    calcular_fitness_func=ga.calcular_fitness,
                    fechar_ao_terminar=finalizar,
                    mostrar_evolucao=True
                )
                
                # Pequena pausa para permitir a atualização da tela
                time.sleep(0.05)
                
                return continuar
                
            except Exception as e:
                print(f"Erro na visualização: {e}")
                return False
                
        return True
    
    # Executa o algoritmo genético
    melhor_grade = ga.algoritmo_genetico(
        tamanho_populacao=tamanho_populacao,
        geracoes=geracoes,
        callback_visualizacao=callback_visualizacao
    )
    
    # Calcula o fitness final
    fitness = ga.calcular_fitness(melhor_grade)
    
    print("\n" + "="*50)
    print(f"Melhor solução encontrada (Fitness: {fitness})")
    print("="*50)
    
    # Mostra a visualização final se solicitado
    if mostrar_visualizacao:
        print("\nAbrindo visualização da grade horária...")
        print("Pressione Ctrl+C no terminal para encerrar.\n")
        
        try:
            # Mostra a visualização final
            visualizar_grade(
                melhor_grade,
                geracoes,
                fitness,
                populacao=populacao_atual,
                calcular_fitness_func=ga.calcular_fitness,
                fechar_ao_terminar=False,
                mostrar_evolucao=True
            )
            
            # Mantém a janela aberta até o usuário fechar
            try:
                plt.show(block=True)
            except KeyboardInterrupt:
                print("\nVisualização encerrada pelo usuário.")
                plt.close('all')
            
        except Exception as e:
            print(f"Erro ao exibir a visualização final: {e}")
        finally:
            # Finaliza a visualização corretamente
            finalizar_visualizacao()
    
    return melhor_grade

if __name__ == "__main__":
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Algoritmo Genético para Grade Horária')
    parser.add_argument('--populacao', type=int, default=50, help='Tamanho da população')
    parser.add_argument('--geracoes', type=int, default=100, help='Número de gerações')
    parser.add_argument('--visualizar', action='store_true', help='Mostrar visualização gráfica ao final')
    parser.add_argument('--salvar-imagem', type=str, help='Salvar grade horária como imagem (caminho do arquivo)')
    
    args = parser.parse_args()
    
    try:
        # Executa o algoritmo genético
        melhor_grade = executar_algoritmo_genetico(
            tamanho_populacao=args.populacao,
            geracoes=args.geracoes,
            mostrar_visualizacao=args.visualizar
        )
        
        # Salva a imagem se solicitado
        if args.salvar_imagem:
            try:
                caminho_imagem = salvar_imagem_grade(
                    melhor_grade, 
                    args.salvar_imagem,
                    args.geracoes,
                    ga.calcular_fitness(melhor_grade)
                )
                print(f"\nGrade horária salva como: {caminho_imagem}")
            except Exception as e:
                print(f"\nErro ao salvar imagem: {e}")
        
        # Mostra detalhes da solução
        print("\nDetalhes da solução:")
        # Ordena as aulas por dia e horário para facilitar a visualização
        aulas_ordenadas = sorted(melhor_grade, key=lambda x: (x['dia'], x['horario']))
        
        # Cabeçalho da tabela
        print("-" * 80)
        print(f"{'Dia':<10} | {'Horário':<15} | {'Disciplina':<30} | {'Professor':<20} | Sala")
        print("-" * 80)
        
        # Dados das aulas
        for aula in aulas_ordenadas:
            print(f"{aula['dia']:<10} | {aula['horario']:<15} | {aula['disciplina']:<30} | {aula.get('professor', 'N/A'):<20} | {aula['sala']}")
        
        print("-" * 80)
        
        print("\nExecução concluída com sucesso!")
            
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    finally:
        # Garante que os recursos sejam liberados corretamente
        finalizar_visualizacao()