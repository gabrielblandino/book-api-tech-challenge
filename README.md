# Tech Challenge: API Pública para Consulta de Livros

Este projeto consiste na criação de uma infraestrutura completa para extração, transformação e disponibilização de dados de livros, servidos através de uma API RESTful pública.

## 1. Arquitetura do Projeto

A solução foi desenhada para ser modular, eficiente e escalável, seguindo as melhores práticas de engenharia de machine learning para a preparação de dados.

**Diagrama do Pipeline de Dados:**
`[Site: books.toscrape.com] -> [Script de Web Scraping (Python/BeautifulSoup)] -> [Armazenamento em CSV (data/books.csv)]`

**Diagrama da Arquitetura da API:**
`[Usuário/Cliente] -> [Internet] -> [Heroku Platform] -> [API RESTful (FastAPI)] -> [Leitura de Dados (Pandas DataFrame)] -> [Resposta JSON]`

### Pipeline de Dados (ETL)

O processo de ingestão de dados segue um modelo de Extração, Transformação e Carga (ETL):

* **Extração (Extract):** O script `scripts/scrapping.py` navega por todas as 50 páginas de listagem de livros. Para cada livro, ele extrai dados básicos e o link para a página de detalhes. Em seguida, acessa essa página de detalhes para obter os dados completos.
* **Transformação (Transform):** Os dados brutos (HTML) são parseados com `BeautifulSoup`. O preço é limpo para remover símbolos de moeda, e todos os dados (título, preço, avaliação, disponibilidade, categoria e imagem) são estruturados.
* **Carga (Load):** Um DataFrame do Pandas é criado com os dados de todos os livros. Uma coluna `id` é gerada para identificação única, e o DataFrame final é salvo como `data/books.csv`, que serve como a fonte de dados para a API.

### Arquitetura da API

* **Framework:** A API foi desenvolvida com **FastAPI**, um framework moderno e de alta performance para Python. Ele foi escolhido por sua velocidade, validação de dados nativa com Pydantic e geração automática de documentação interativa (Swagger UI).
* **Fonte de Dados:** Na inicialização, a API carrega o arquivo `data/books.csv` em um DataFrame do Pandas que fica em memória. Esta abordagem garante latência ultrabaixa para todas as operações de leitura, sendo ideal para o escopo deste projeto.
* **Deploy:** A aplicação está hospedada na plataforma **Heroku**, garantindo disponibilidade pública, escalabilidade e um ambiente de produção robusto.
* **Autenticação:** Endpoints sensíveis, como o que dispara o scraping, são protegidos por autenticação via token JWT (JSON Web Token), conforme o desafio bônus.

### Plano de Escalabilidade Futura

1.  **Banco de Dados:** Substituir o `books.csv` por um banco de dados gerenciado (como Heroku Postgres) para permitir operações de escrita mais complexas e maior volume de dados.
2.  **Cache:** Implementar um cache com Redis para os endpoints mais requisitados, como `GET /api/v1/books` e `GET /api/v1/stats/overview`, reduzindo a carga na aplicação.
3.  **Tarefas em Background:** Migrar a execução do scraper para uma fila de tarefas (como Celery com RabbitMQ), permitindo que processos de longa duração rodem de forma assíncrona sem bloquear a API.