# Sistema de Alocação de Horários com Algoritmo Genético

Este é um sistema de otimização de grade horária acadêmica que utiliza Algoritmo Genético para criar horários de aula considerando diversas restrições e preferências.

## 📋 Visão Geral

O sistema foi desenvolvido para resolver o problema de alocação de disciplinas em salas e horários, considerando:
- Preferências de horário dos professores
- Disponibilidade de salas e laboratórios
- Restrições de tipo de sala (teórica/laboratório)
- Evitar conflitos de alocação

## 🚀 Novidades

- **Visualização Interativa**: Nova interface gráfica usando Pygame para visualização da grade horária
- **Melhor Desempenho**: Otimizações no algoritmo genético para resultados mais rápidos e precisos
- **Exportação de Imagens**: Salve a grade horária como imagem para compartilhamento

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Dependências do sistema para o Pygame (caso necessário):
  - Ubuntu/Debian: `sudo apt-get install python3-pygame`
  - Fedora: `sudo dnf install python3-pygame`
  - macOS: `brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf`

### Configuração do Ambiente

1. **Clone o repositório**
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd genetic_algorithm
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
   - `pygame`: Para visualização interativa da grade horária
   
   E também as dependências de desenvolvimento:
   - `pytest`: Para execução de testes
   - `black`: Para formatação de código
   - `flake8`: Para análise de código
   - `sphinx` e `sphinx-rtd-theme`: Para geração de documentação

## 🚀 Como Usar

### Execução Básica
```bash
python main.py
```

### Opções de Linha de Comando
```bash
python main.py --populacao 50 --geracoes 100 --visualizar --salvar-imagem grade.png
```

**Parâmetros:**
- `--populacao`: Tamanho da população (padrão: 50)
- `--geracoes`: Número de gerações (padrão: 100)
- `--visualizar`: Mostra a visualização gráfica ao final
- `--salvar-imagem`: Salva a grade horária como imagem

### Controles da Visualização
- **ESC**: Fecha a visualização
- **Clique no X**: Fecha a visualização

## 📊 Estrutura do Código

### Arquivos Principais
- `main.py`: Ponto de entrada do programa, interface de linha de comando
- `genetic_algorithm.py`: Implementação do algoritmo genético
- `visualization.py`: Visualização interativa da grade horária
- `requirements.txt`: Dependências do projeto

### Dados do Problema
- `DISCIPLINAS`: Lista de disciplinas com suas restrições
- `SALAS`: Salas e laboratórios disponíveis
- `DIAS`: Dias da semana
- `HORARIOS_MANHA`/`HORARIOS_TARDE`: Faixas horárias

## 🔍 Solução de Problemas

### A grade está vazia na visualização?
Verifique se:
1. O formato dos horários está correto (ex: "08:00-10:00")
2. Os dias da semana estão escritos corretamente (ex: "Segunda", "Terça", etc.)
3. As disciplinas têm todos os campos necessários (disciplina, professor, sala, dia, horário)

### Erros ao executar o Pygame
Certifique-se de que todas as dependências do sistema estão instaladas (veja a seção de instalação).

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
