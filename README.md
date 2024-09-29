# Análise Exploratória e Construção da Narrativa de Dados para Sistema de Decisão de Investimento em Criptoativos

## 1. Análise Exploratória dos Dados (Exploratory Data Analysis - EDA)

O primeiro passo para construir um sistema eficiente de tomada de decisão para investimento em criptoativos foi analisar e entender o comportamento histórico dos preços do criptoativo selecionado, o **BTC-USD** (Bitcoin em relação ao Dólar Americano). Essa análise exploratória foi crucial para identificar padrões, sazonalidades, e características dos dados que nos orientariam na escolha do modelo de machine learning a ser utilizado.

### 1.1 Coleta dos Dados
Os dados de preços históricos do BTC-USD foram coletados utilizando a biblioteca **yfinance** do Python, que permite extrair informações financeiras diretamente de fontes online confiáveis, como o Yahoo Finance.

Os dados coletados incluem as seguintes colunas:
- **Date:** A data da observação.
- **Close:** O preço de fechamento do criptoativo para o dia específico.

### 1.2 Limpeza e Pré-processamento dos Dados
Após a coleta dos dados, foi realizada uma etapa de pré-processamento para garantir que a série temporal estivesse limpa e pronta para análise e modelagem. As principais etapas incluíram:
- **Remoção de Dados Ausentes:** Identificação e remoção de registros nulos ou faltantes.
- **Conversão de Tipos de Dados:** Conversão da coluna `Date` para o tipo `datetime` para facilitar a manipulação temporal.
- **Ordenação dos Dados:** Ordenação dos registros pela data para manter a sequência temporal.

### 1.3 Visualização dos Dados
Para entender melhor os padrões e a evolução do BTC-USD ao longo do tempo, foram gerados gráficos de linha dos preços de fechamento ao longo do período de coleta.

#### Exemplo de Visualizações
1. **Gráfico de Linha do Preço de Fechamento**: Este gráfico mostra a evolução dos preços ao longo do tempo, destacando tendências e volatilidade do mercado.
2. **Média Móvel**: Foram calculadas médias móveis para observar tendências de curto e longo prazo, ajudando a suavizar a volatilidade diária.
3. **Histograma de Retornos Diários**: Para entender a distribuição dos retornos, foram plotados histogramas dos retornos diários do BTC-USD.

### 1.4 Insights da Análise Exploratória
Durante a análise exploratória, observamos que:
- **Alta Volatilidade**: O BTC-USD possui uma volatilidade significativa, com mudanças de preço rápidas e imprevisíveis.
- **Tendências Temporais**: Há períodos de crescimento e queda acentuados, indicando a existência de tendências temporais relevantes.
- **Padrões Não Lineares**: A análise visual indicou que os dados possuem padrões complexos e não lineares, o que sugere a necessidade de modelos avançados para captura dessas tendências.

---

## 2. Construção da Narrativa de Dados e Justificativa da Escolha do Modelo

A partir da análise exploratória, foram traçadas as estratégias para a modelagem dos dados e escolha do modelo de machine learning mais adequado.

### 2.1 Justificativa para a Escolha do Modelo
Visto que os dados do BTC-USD apresentam características complexas de séries temporais, optamos por testar e comparar diferentes modelos de previsão de séries temporais:

1. **Modelos de Regressão Simples (Base de Comparação):**
   Foram testados modelos de regressão linear simples e modelos de média móvel para fornecer uma base de comparação de desempenho. Estes modelos apresentaram desempenho limitado devido à sua incapacidade de capturar padrões não lineares.

2. **Modelos Tradicionais de Séries Temporais (ARIMA e Prophet):**
   Modelos clássicos de séries temporais, como ARIMA e Prophet, foram aplicados para verificar sua capacidade de capturar padrões temporais. Embora estes modelos sejam eficazes para séries com padrões sazonais e tendências lineares, tiveram dificuldade em capturar a volatilidade e complexidade dos dados do BTC-USD.

3. **Redes Neurais LSTM (Long Short-Term Memory):**
   Após análises e testes iniciais, decidimos utilizar uma **Rede Neural Recorrente LSTM**. As LSTMs são conhecidas por sua habilidade de capturar dependências de longo prazo em dados temporais, o que é ideal para o BTC-USD, devido à sua natureza volátil e aos padrões não lineares observados nos dados.

   - **Capacidade de Captura de Padrões Não Lineares**: As LSTMs são especialmente boas em capturar padrões não lineares e complexos que modelos de regressão e ARIMA não conseguem detectar.
   - **Manutenção de Contexto Temporal**: Como os dados de preços de criptoativos são altamente dependentes do tempo, o uso de LSTMs permite que a memória da rede capture essas dependências temporais.

### 2.2 Treinamento e Teste do Modelo
O modelo LSTM foi treinado com os dados de fechamento diários do BTC-USD. O conjunto de dados foi dividido em **treinamento** e **teste**, com 80% dos dados utilizados para treinamento e 20% para validação. 

As principais métricas avaliadas durante os testes foram:
- **Mean Squared Error (MSE)**: Utilizado para medir o erro médio entre os valores previstos e reais.
- **Mean Absolute Error (MAE)**: Uma métrica que mostra a magnitude do erro médio.

Os resultados dos testes mostraram que o modelo LSTM foi capaz de capturar as tendências gerais dos dados, com desempenho superior aos modelos tradicionais de séries temporais.

### 2.3 Visualização e Interpretação dos Resultados
Para tornar os resultados acessíveis e interpretáveis para os usuários, foi desenvolvido um dashboard interativo, onde os resultados das previsões são apresentados em um gráfico de linha que destaca tanto os preços históricos quanto as previsões feitas pelo modelo.

Os usuários podem visualizar:
- **Preços Históricos vs Previsões**: Um gráfico comparando os preços reais e previstos ao longo do tempo.
- **Valores Preditos Detalhados**: Uma tabela exibindo as previsões de preços para os próximos dias.

O dashboard permite que os usuários escolham diferentes criptoativos para análise e ajustem parâmetros para simular diferentes cenários de investimento.

---

## 3. Como Executar o Projeto com Docker

Esta seção fornece as instruções para construir e executar o projeto utilizando Docker. O Docker é usado para garantir um ambiente de desenvolvimento consistente e facilitar a execução do projeto em qualquer sistema operacional.

### Pré-requisitos

- **Docker**: Certifique-se de ter o Docker instalado. Consulte o [guia oficial](https://docs.docker.com/get-docker/) para instruções de instalação.
- **Docker Compose**: Também é necessário ter o Docker Compose instalado, geralmente incluído junto com o Docker Desktop.

### Construindo e Executando o Projeto

#### Passo 1: Clonar o Repositório

Primeiro, clone o repositório do projeto em sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

#### Passo 2: Configurar Variáveis de Ambiente

No diretório raiz do projeto, crie um arquivo `.env` para configurar variáveis de ambiente necessárias (como as credenciais do banco de dados):

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=cripto_db
```

#### Passo 3: Construir as Imagens Docker

Para construir as imagens Docker do projeto, incluindo o backend e o banco de dados PostgreSQL, execute:

```bash
docker-compose build
```

#### Passo 4: Iniciar os Containers

Após a construção das imagens, inicie os containers do projeto:

```bash
docker-compose up
```

Este comando iniciará os seguintes containers:

- **Backend**: O backend da aplicação (FastAPI) rodando no container.
- **PostgreSQL**: O banco de dados PostgreSQL rodando em seu próprio container.
- **Frontend** (opcional): Se você tiver configurado um frontend, ele também será iniciado.

#### Passo 5: Acessar a Aplicação

- **API:** A API do backend estará acessível em `http://localhost:8000`.
- **Dashboard:** Se o frontend estiver configurado, você pode acessá-lo em `http://localhost:3000` (ou outra porta especificada no arquivo `docker-compose.yml`).

### Comandos Úteis

- **Parar os Containers:**

  ```bash
  docker-compose down
  ```

- **Verificar os Logs:**

  Para verificar os logs de um container específico, use:

  ```bash
  docker-compose logs nome_do_container
  ```

- **Executar Migrações (se aplicável):**

  Para executar migrações no banco de dados, você pode acessar o container do backend:

  ```bash
  docker-compose exec backend bash
  ```

  E então executar os comandos de migração.

### Estrutura do Docker Compose

O arquivo `docker-compose.yml` inclui a configuração dos serviços (backend, PostgreSQL e frontend) e define como eles interagem. Certifique-se de que ele esteja corretamente configurado para que os serviços possam se comunicar sem problemas.
```

Certifique-se de ajustar os detalhes como o nome do repositório e as variáveis de ambiente conforme necessário para o seu projeto.
