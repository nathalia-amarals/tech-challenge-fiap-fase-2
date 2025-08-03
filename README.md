# Sistema de Alocação de Horários com Algoritmo Genético

Este é um sistema de otimização de grade horária acadêmica que utiliza Algoritmo Genético para criar horários de aula considerando diversas restrições e preferências.

## 📋 Visão Geral

O sistema foi desenvolvido para resolver o problema de alocação de disciplinas em salas e horários, considerando:
- Preferências de horário dos professores
- Disponibilidade de salas e laboratórios
- Restrições de tipo de sala (teórica/laboratório)
- Evitar conflitos de alocação

## 🚀 Novidades

- **Visualização Aprimorada**: Interface gráfica otimizada com melhor exibição de texto e informações
- **Restrições Inteligentes**: Prevenção de sobreposição de aulas no mesmo horário, mesmo em salas diferentes
- **Melhor Legibilidade**: Texto das disciplinas ajustado automaticamente para melhor visualização
- **Exportação de Imagens**: Salve a grade horária como imagem para compartilhamento
- **Validação de Dados**: Verificação rigorosa de horários e dias para garantir consistência

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
- **Barra de Espaço**: Avança para a próxima geração (quando em modo de evolução)
- **Seta para a Direita**: Avança para a próxima geração
- **Seta para a Esquerda**: Volta para a geração anterior

## 📊 Estrutura do Código

### Arquivos Principais
- `main.py`: Ponto de entrada do programa, interface de linha de comando
- `genetic_algorithm.py`: Implementação do algoritmo genético com restrições e funções de fitness
- `visualization.py`: Visualização interativa da grade horária com suporte a texto dinâmico
- `config.py`: Configurações globais e constantes do sistema
- `requirements.txt`: Dependências do projeto

### Restrições Implementadas
1. **Conflitos de Professor**: Nenhum professor pode dar aula em dois lugares ao mesmo tempo
2. **Conflitos de Sala**: Nenhuma sala pode ser usada por mais de uma disciplina simultaneamente
3. **Laboratórios Específicos**: Apenas disciplinas que requerem laboratório podem ser alocadas em salas de laboratório
4. **Sem Sobreposição**: Não são permitidas duas disciplinas no mesmo horário, mesmo em salas diferentes

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
4. Não há conflitos de horário que estejam removendo disciplinas da grade

### Texto cortado nas células
O sistema agora faz quebra automática de texto. Se algum texto ainda estiver sendo cortado:
1. Tente reduzir o tamanho do texto da disciplina
2. Verifique se a resolução da tela é adequada
3. Considere usar abreviações para nomes longos de disciplinas

### Erros ao executar o Pygame
Certifique-se de que todas as dependências do sistema estão instaladas (veja a seção de instalação). Se o problema persistir:
```bash
pip install --upgrade pygame
```

### Disciplinas não aparecendo na grade
Se algumas disciplinas não estão aparecendo, verifique:
1. Se há conflitos de horário que estejam sendo penalizados
2. Se os horários estão dentro dos intervalos permitidos
3. Se as restrições de sala estão sendo respeitadas

## 📄 Licença

Este projeto está licenciado sob a licença AGPL-3.0 license - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
