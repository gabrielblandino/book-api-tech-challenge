# Plano Arquitetural do Sistema

## 1. Introdução

Este documento detalha o plano arquitetural para a API de Consulta de Livros, abordando o fluxo de dados completo, a estratégia de escalabilidade e a integração com futuras aplicações de Machine Learning. A arquitetura foi concebida para ser robusta, modular e evolutiva.

## 2. Pipeline de Dados: Da Ingestão ao Consumo

O fluxo de dados do sistema segue um modelo ETL (Extract, Transform, Load) bem definido, garantindo que os dados sejam coletados, processados e disponibilizados de forma eficiente e estruturada.

**Diagrama de Fluxo:**

`[Fonte de Dados Externa] -> [Módulo de Extração] -> [Módulo de Transformação] -> [Camada de Armazenamento] -> [Camada de Serviço (API)] -> [Consumidor Final]`

**Detalhamento das Fases do Pipeline:**

* **Fase 1: Ingestão (Extract)**
    * **Fonte de Dados:** O site de e-commerce `books.toscrape.com`.
    * **Mecanismo:** Um script dedicado (`scripts/scrapping.py`) é responsável por realizar a coleta dos dados. Ele utiliza a biblioteca `requests` para estabelecer a comunicação HTTP e a `BeautifulSoup4` para realizar o parsing do conteúdo HTML bruto das páginas.
    * **Operação:** O processo é iniciado com a varredura das páginas de listagem para identificar todos os livros disponíveis. As URLs individuais de cada livro são coletadas para a fase de extração detalhada.

* **Fase 2: Processamento (Transform)**
    * **Tecnologia:** A biblioteca `Pandas` é utilizada para a estruturação e manipulação dos dados.
    * **Operação:** O script de extração processa cada página de livro para extrair, limpar e normalizar os atributos relevantes: título, preço (convertido para tipo numérico), avaliação, status de disponibilidade, categoria e a URL da imagem de capa. Os dados limpos são então consolidados em um DataFrame estruturado.

* **Fase 3: Carga e Armazenamento (Load)**
    * **Formato:** Os dados processados são persistidos em um arquivo de valores separados por vírgula (`data/books.csv`).
    * **Justificativa:** Para o escopo inicial do projeto, o formato CSV oferece um meio leve e portátil de armazenamento, desacoplando o processo de scraping da disponibilidade da API e servindo como uma fonte de dados estável para a aplicação.

* **Fase 4: Disponibilização (API Service Layer)**
    * **Tecnologia:** A camada de serviço é implementada através de uma API RESTful desenvolvida com o framework **FastAPI**.
    * **Operação:** Durante a inicialização, a aplicação carrega os dados do arquivo CSV para um DataFrame em memória, permitindo um acesso de baixa latência. A API expõe um conjunto de endpoints que permitem a consulta, filtragem e agregação desses dados, retornando-os em formato JSON padronizado.

* **Fase 5: Consumo**
    * **Consumidores:** A API é projetada para ser consumida por uma variedade de clientes, incluindo aplicações web (front-end), scripts de análise de dados, notebooks Jupyter ou outras ferramentas de automação que necessitem dos dados de livros.

## 3. Arquitetura para Escalabilidade Futura

A arquitetura atual, embora funcional, foi projetada com provisões para crescimento futuro. A estratégia de escalabilidade se concentra em três áreas principais:

* **Camada de Persistência:** A limitação principal do modelo atual é o uso de um arquivo CSV. A evolução natural é a adoção de um Sistema de Gerenciamento de Banco de Dados (SGBD) profissional.
    * **Solução Proposta:** Migrar os dados para uma instância **PostgreSQL**. Esta mudança introduzirá benefícios como transações ACID, capacidade de indexação para otimização de consultas complexas, segurança aprimorada através de controle de acesso e a capacidade de lidar com volumes de dados muito maiores e operações de escrita concorrentes.

* **Camada de Cache:** Com o aumento do tráfego, o acesso repetido ao banco de dados pode se tornar um gargalo. A implementação de uma camada de cache é fundamental para otimizar a performance.
    * **Solução Proposta:** Integrar o **Redis** como um armazenamento de chave-valor em memória. Respostas de endpoints de alta demanda e baixa volatilidade (ex: `GET /api/v1/categories`, `GET /api/v1/stats/overview`) seriam armazenadas em cache por um tempo predeterminado, reduzindo drasticamente o tempo de resposta e a carga sobre o banco de dados.

* **Processamento Assíncrono:** A execução de tarefas de longa duração, como o web scraping, não deve ocorrer no mesmo processo síncrono da API, pois isso pode levar a timeouts e indisponibilidade.
    * **Solução Proposta:** Implementar uma arquitetura de tarefas em background com **Celery** e um message broker como **RabbitMQ** ou Redis. O endpoint de trigger do scraping passaria a enfileirar uma nova tarefa, que seria executada por um processo "worker" independente, permitindo que a API retorne uma resposta imediata ao usuário enquanto o trabalho pesado é realizado em segundo plano.

## 4. Cenário de Uso para Cientistas de Dados

A API serve como um acelerador para o ciclo de vida de projetos de ciência de dados:

* **Aquisição de Dados:** O cientista de dados pode dispensar a necessidade de criar seu próprio scraper. Uma única chamada ao endpoint `GET /api/v1/books` em um ambiente como um notebook Jupyter permite a obtenção do dataset completo e sua carga imediata em um DataFrame do Pandas.

* **Análise Exploratória e Pré-processamento:** Os endpoints de estatísticas (`/api/v1/stats/*`) oferecem uma visão macroscópica imediata da distribuição dos dados. Para um trabalho mais aprofundado, o endpoint `GET /api/v1/ml/training-data` é de particular importância, pois já fornece uma versão dos dados pré-processada, com features numéricas e flags, pronta para ser usada na exploração de correlações e na preparação para o treinamento de modelos.

## 5. Plano de Integração com Modelos de Machine Learning

A operacionalização de um modelo treinado é o objetivo final deste ecossistema de dados. O plano de integração segue os princípios de MLOps.

1.  **Treinamento e Versionamento do Modelo:** Após a fase de experimentação, um modelo de Machine Learning (ex: um sistema de recomendação baseado em conteúdo ou um modelo de previsão de preços) é treinado. O artefato do modelo treinado (ex: um arquivo `.pkl` ou `.onnx`) é versionado junto ao código-fonte ou em um registro de modelos.

2.  **Carregamento do Modelo na API:** A aplicação FastAPI é estendida para carregar o artefato do modelo em memória durante seu ciclo de inicialização. Isso garante que o modelo esteja pronto para inferência sem a latência de carregá-lo a cada requisição.

3.  **Endpoint de Inferência em Tempo Real:** O endpoint `POST /api/v1/ml/predictions` (atualmente um mock) é implementado para servir como a interface de inferência. Ele é projetado para:
    a. Receber dados de entrada em formato JSON, representando as features de uma nova instância a ser predita.
    b. Realizar as mesmas etapas de pré-processamento aplicadas durante o treinamento para garantir a consistência dos dados.
    c. Passar os dados processados para o método de predição do modelo carregado.
    d. Retornar a predição do modelo como uma resposta JSON ao cliente.

Este processo transforma o modelo treinado de um artefato estático em um serviço dinâmico e consumível, completando o ciclo de vida do Machine Learning.