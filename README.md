# Tech Challenge - Fase 1: API de Livros

API RESTful para consulta de dados de livros, desenvolvida como solução para o Tech Challenge da Pós-Graduação em Engenharia de Machine Learning.

## Descrição do Projeto

Este projeto consiste na criação de uma infraestrutura completa de dados para um futuro sistema de recomendação de livros. O desafio inicial foi construir um pipeline para extrair, transformar e disponibilizar dados de livros via uma API pública, garantindo escalabilidade e facilidade de uso para cientistas de dados.

A aplicação realiza web scraping do site [books.toscrape.com](http://books.toscrape.com/), armazena os dados e os expõe através de endpoints RESTful funcionais e documentados.

**URL da API em Produção:** `https://book-api-tech-83e5f237d218.herokuapp.com/docs`

## Arquitetura e Pipeline de Dados

A solução foi projetada de forma modular, seguindo as melhores práticas para ingestão, processamento e consumo de dados.

**Pipeline de Dados (ETL):**
`[Site: books.toscrape.com] -> [Script de Web Scraping (Python/BeautifulSoup)] -> [Armazenamento (data/books.csv)] -> [API]`

**Arquitetura da Aplicação:**
`[Cliente (Postman/Frontend)] -> [Internet] -> [Plataforma de Deploy (Heroku)] -> [API RESTful (FastAPI)] -> [Leitura dos Dados (Pandas)] -> [Resposta JSON]`

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI:** Framework web para a construção da API.
- **Uvicorn & Gunicorn:** Servidores ASGI/WSGI para rodar a aplicação em desenvolvimento e produção.
- **Pandas:** Para manipulação e armazenamento dos dados em memória.
- **BeautifulSoup4 & Requests:** Para o processo de web scraping.
- **Passlib & PyJWT:** Para a implementação de autenticação e segurança com tokens JWT.
- **Heroku:** Plataforma de nuvem (PaaS) para o deploy e hospedagem da aplicação.

## Instalação e Configuração

Siga os passos abaixo para executar o projeto localmente.

1.  **Clone o repositório:**
    ```bash
    git clone https://https://github.com/gabrielblandino/book-api-tech-challenge.git
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves para o sistema de autenticação:
    ```
    SECRET_KEY_AUTH="sua_chave_secreta_aqui"
    ALGORITHM_KEY="HS256"
    ```

## Instruções de Execução

Com o ambiente configurado, você pode executar os componentes do projeto.

1.  **Executar o Web Scraper (opcional, pois os dados já estão no repositório):**
    Este comando irá extrair os dados do site e (re)gerar o arquivo `data/books.csv`.
    ```bash
    python scripts/scrapping.py
    ```

2.  **Executar a API localmente:**
    Este comando iniciará o servidor de desenvolvimento.
    ```bash
    uvicorn api.main:app --reload
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

##  API - Documentação das Rotas

A documentação interativa completa, gerada automaticamente pelo FastAPI, está disponível em:
- **Swagger UI:** `http://127.0.0.1:8000/docs` ou `https://book-api-tech-83e5f237d218.herokuapp.com/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc` ou `https://book-api-tech-83e5f237d218.herokuapp.com/redoc`

Abaixo estão exemplos de como chamar cada rota principal usando `curl`.

---
### **1. Rotas de Status e Saúde da API**
---
#### `GET /api/v1/health`
Verifica a saúde da aplicação.
- **Autenticação:** Não requerida.
- **Exemplo de Chamada (`curl`):**
  ```bash
  curl -X GET "[https://book-api-tech-83e5f237d218.herokuapp.com/api/v1/health](https://book-api-tech-83e5f237d218.herokuapp.com/api/v1/health)"
