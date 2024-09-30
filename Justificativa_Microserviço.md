# Documentação do Deployment de Microsserviço/Data Lake

## Visão Geral do Projeto

Este projeto envolve a construção de uma aplicação para auxiliar na tomada de decisões de investimento em criptoativos. A arquitetura do projeto segue o padrão de microsserviços, onde diferentes funcionalidades são isoladas em serviços separados. Um dos principais componentes deste projeto é o **Microsserviço** que fornece previsões de preços de criptoativos, encapsulado em containers Docker para facilitar a escalabilidade e a portabilidade.

O projeto também pode ser adaptado para uso de um **Data Lake**, caso o volume de dados históricos ou a diversidade de fontes de dados sejam fatores críticos. Para este cenário, o projeto implementa um ambiente de **Data Lake** com uma estrutura para ingestão, armazenamento e processamento de dados.

## Justificativa para a Escolha do Microsserviço e Data Lake

### 1. Justificativa do Microsserviço

A escolha da arquitetura de **Microsserviço** foi baseada nos seguintes fatores:

- **Isolamento de Funcionalidades**: A separação de responsabilidades permite que a lógica de previsão de preços seja isolada de outras partes da aplicação, como o frontend e a interface de usuário. Isso facilita a manutenção e evolução do projeto.
  
- **Escalabilidade Independente**: O uso de microsserviços permite que cada serviço seja escalado independentemente, de acordo com a demanda. Por exemplo, o serviço de previsão pode ser escalado horizontalmente durante picos de uso, sem impactar outras partes do sistema.

- **Facilidade de Integração**: O microsserviço pode ser facilmente integrado com outras fontes de dados, APIs ou bancos de dados, além de possibilitar a troca de tecnologias ou frameworks sem grandes refatorações na aplicação.

A escolha de usar **FastAPI** para o desenvolvimento do microsserviço foi motivada por:

- **Desempenho**: FastAPI é uma framework de alta performance baseada em Python, permitindo a construção de APIs RESTful rápidas e eficientes.
  
- **Facilidade de Desenvolvimento**: A integração nativa com tipos do Python e a validação automática de dados facilitam a implementação e manutenção dos endpoints da API.
  
- **Documentação Automática**: A documentação dos endpoints é gerada automaticamente pelo Swagger UI, tornando a API mais acessível e fácil de usar.

### 2. Justificativa para a Implementação de um Data Lake (Opcional)

Um **Data Lake** foi considerado para armazenar e processar grandes volumes de dados históricos de preços de criptoativos ou outros ativos financeiros. A escolha de um Data Lake é justificada pelos seguintes motivos:

- **Armazenamento de Dados Heterogêneos**: Diferentes fontes de dados (JSON, CSV, APIs, etc.) podem ser armazenadas em seu formato original, oferecendo flexibilidade no armazenamento e processamento de dados.
  
- **Análises e Processamentos Complexos**: Um Data Lake permite a execução de análises mais complexas e o uso de técnicas avançadas de machine learning, já que todos os dados necessários estão centralizados.

- **Escalabilidade e Custo**: O uso de uma solução de Data Lake como o **Amazon S3** ou o **Google Cloud Storage** possibilita a escalabilidade horizontal, além de oferecer custo-eficiência para o armazenamento de grandes volumes de dados.

A escolha de um **Data Lake** é recomendada se o projeto pretende lidar com dados em grande escala, ou seja, múltiplas fontes, análises mais complexas ou necessidade de dados históricos extensos.

## Descrição dos Arquivos de Deployment

### Dockerfile

O `Dockerfile` utilizado neste projeto tem como objetivo encapsular o microsserviço de previsão de preços. Abaixo está uma descrição do `Dockerfile`:

```dockerfile
# Usar a imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requirements
COPY requirements.txt .

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos da aplicação
COPY . .

# Expor a porta 8000 para comunicação com o serviço FastAPI
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
