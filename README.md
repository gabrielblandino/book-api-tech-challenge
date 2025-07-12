
# Book API - Tech Challenge FIAP

Este repositório contém o projeto desenvolvido para o Tech Challenge da pós-graduação em Machine Learning Engineering da FIAP. A proposta foi criar um pipeline de dados completo, extraindo informações do site [Books to Scrape](https://books.toscrape.com/) e disponibilizando esses dados por meio de uma API pública com foco em consumo por cientistas de dados e sistemas de recomendação.

## Tecnologias Utilizadas

- Python 3.8+
- FastAPI
- Uvicorn
- BeautifulSoup + Requests
- Pandas

## Organização do Projeto

```
book-api-tech-challenge/
├── api/
│   └── main.py             # API com todos os endpoints
├── scripts/
│   └── scrapping.py        # Script responsável por extrair os dados
├── data/
│   └── books.csv           # Base local com os dados extraídos
├── docs/
│   └── arquitetura.pdf     # Diagrama e explicações da arquitetura do projeto
├── requirements.txt
└── README.md
```

## Como rodar o projeto localmente

1. Clone o repositório:
```bash
git clone https://github.com/gabrielblandino/book-api-tech-challenge.git
cd book-api-tech-challenge
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate  # Linux/macOS
```

3. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

4. Execute o scraper para gerar os dados:
```bash
python scripts/scrapping.py
```

5. Inicie a API localmente:
```bash
uvicorn api.main:app --reload
```

6. Acesse a documentação interativa:
```
http://127.0.0.1:8000/docs
```

## Endpoints principais

| Método | Rota                                      | Descrição |
|--------|-------------------------------------------|-----------|
| GET    | `/api/v1/health`                          | Verifica se a API está funcionando |
| GET    | `/api/v1/books`                           | Retorna todos os livros da base |
| GET    | `/api/v1/books/{id}`                      | Retorna os dados de um livro específico |
| GET    | `/api/v1/categories`                      | Lista todas as categorias disponíveis |
| GET    | `/api/v1/books/search?title=&category=`   | Busca livros por título e/ou categoria |

Todos esses endpoints podem ser testados diretamente pela interface Swagger.

## Exemplos de resposta

### Listagem de livros
`GET /api/v1/books`
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": "Three",
    "availability": "In stock",
    "category": "Poetry",
    "image_url": "http://books.toscrape.com/media/cache/...jpg"
  }
]
```

### Verificação de status
`GET /api/v1/health`
```json
{ "status": "ok" }
```

## Deploy

O deploy em nuvem será feito utilizando Render ou Fly.io. O link de produção será atualizado aqui assim que estiver disponível.

## Arquitetura

O diagrama explicando a arquitetura do projeto estará disponível na pasta `/docs`.

## Vídeo de apresentação

Link da apresentação (será adicionado posteriormente).

## O que foi entregue até agora

- Coleta automatizada de dados via web scraping
- API REST estruturada com FastAPI
- Interface de documentação automática (Swagger)
- Endpoints opcionais de estatísticas e recursos para modelos de ML
- Sistema de autenticação com JWT
- Preparação para deploy e apresentação final
