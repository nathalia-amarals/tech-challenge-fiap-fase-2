# Sistema de Alocação de Horários com Algoritmo Genético

Este é um sistema de otimização de grade horária acadêmica que utiliza Algoritmo Genético para criar horários de aula considerando diversas restrições e preferências.

## 📋 Visão Geral

O sistema foi desenvolvido para resolver o problema de alocação de disciplinas em salas e horários, considerando:
- Preferências de horário dos professores
- Disponibilidade de salas e laboratórios
- Restrições de tipo de sala (teórica/laboratório)
- Evitar conflitos de alocação
- Exibição clara das informações dos professores

## 🚀 Novidades na Versão Atual

- **Visualização Aprimorada com Matplotlib**: Nova interface gráfica mais limpa e responsiva
- **Informações de Professores**: Exibição clara do professor responsável por cada disciplina
- **Saída Formatada no Terminal**: Tabela organizada mostrando a grade horária completa
- **Código Otimizado**: Melhor desempenho e organização do código
- **Melhor Legibilidade**: Texto ajustado automaticamente para melhor visualização
- **Exportação de Imagens**: Salve a grade horária como imagem para compartilhamento
- **Validação de Dados**: Verificação rigorosa de horários e dias para garantir consistência

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Dependências do sistema para o Matplotlib (caso necessário)

### Configuração do Ambiente

1. **Clone o repositório**
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd tech-challenge-fiap-fase-2
   ```

2. **Crie e ative um ambiente virtual (recomendado)**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
   
   Isso instalará automaticamente:
   - `numpy`: Para operações numéricas
   - `matplotlib`: Para visualização de dados
   - `pygame`: Para suporte a visualização (opcional)

## 🚀 Como Usar

### Execução Básica
```bash
python main.py
```

### Opções de Linha de Comando
```bash
python main.py --populacao 10 --geracoes 50 --visualizar --salvar-imagem grade.png
```

**Parâmetros:**
- `--populacao`: Tamanho da população (padrão: 50)
- `--geracoes`: Número de gerações (padrão: 100)
- `--visualizar`: Mostra a visualização gráfica ao final
- `--salvar-imagem`: Salva a grade horária como imagem

### Saída no Terminal
A saída no terminal agora mostra uma tabela formatada com os detalhes da grade horária, incluindo:
- Dia da semana
- Horário
- Nome da disciplina
- Professor responsável
- Sala de aula

## 📊 Estrutura do Código

### Arquivos Principais
- `main.py`: Ponto de entrada do programa, interface de linha de comando
- `genetic_algorithm.py`: Implementação do algoritmo genético
- `visualization_clean.py`: Visualização otimizada usando Matplotlib
- `visualization.py`: Visualização antiga usando Pygame (mantida para compatibilidade)
- `requirements.txt`: Dependências do projeto

### Exemplo de Saída no Terminal
```
Detalhes da solução:
--------------------------------------------------------------------------------
Dia        | Horário         | Disciplina                     | Professor            | Sala
--------------------------------------------------------------------------------
Segunda    | 08:00-10:00     | Algoritmos e Programação       | Alice                | Lab. Software
Segunda    | 10:00-12:00     | Cálculo I                      | Ana                  | Sala 101
...
```

## 🔍 Solução de Problemas

### A grade está vazia na visualização?
Verifique se:
1. O formato dos horários está correto (ex: "08:00-10:00")
2. Os dias da semana estão escritos corretamente (ex: "Segunda", "Terça", etc.)
3. As disciplinas têm todos os campos necessários (disciplina, professor, sala, dia, horário)

### Texto não está cabendo nas células
O sistema faz ajuste automático de fonte, mas se o texto ainda não estiver legível:
1. Considere usar abreviações para nomes longos de disciplinas
2. Reduza o número de caracteres nas descrições

### Erros ao executar
Certifique-se de que todas as dependências estão instaladas corretamente:
```bash
pip install -r requirements.txt
```

## 📄 Licença

Este projeto está licenciado sob a licença AGPL-3.0 license - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
