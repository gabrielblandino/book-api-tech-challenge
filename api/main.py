from typing import Optional
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
import subprocess
import sys

from api.auth import create_access_token, verify_token, fake_user, pwd_context

app = FastAPI(
    title="Books API - Tech Challenge",
    version="1.0.0",
    description="Uma API para consulta de dados de livros, extraídos via web scraping."
)

try:
    BOOKS_DF = pd.read_csv('data/books.csv')
except FileNotFoundError:
    BOOKS_DF = pd.DataFrame()

@app.get("/api/v1/health", summary="Verifica a saúde da API")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/categories", summary="Lista todas as categorias de livros")
def list_categories():
    if BOOKS_DF.empty:
        return {"categories": []}
    categories = BOOKS_DF['category'].dropna().unique().tolist()
    return {"categories": categories}

@app.get("/api/v1/books", summary="Lista todos os livros")
def list_books():
    if BOOKS_DF.empty:
        return []
    return BOOKS_DF.to_dict(orient='records')

@app.get("/api/v1/books/search", summary="Busca livros por título e/ou categoria")
def search_books(title: str = None, category: str = None):
    if BOOKS_DF.empty:
        return []
    
    df = BOOKS_DF.copy()
    if title:
        df = df[df['title'].str.contains(title, case=False, na=False)]
    if category:
        df = df[df['category'].str.contains(category, case=False, na=False)]
    return df.to_dict(orient='records')

@app.get("/api/v1/books/top-rated", summary="Lista os 10 livros com melhor avaliação")
def top_rated_books():
    if BOOKS_DF.empty:
        return []
    top_books = BOOKS_DF[BOOKS_DF['rating'] == 'Five'].head(10)
    return top_books.to_dict(orient='records')

@app.get("/api/v1/books/price-range", summary="Filtra livros por faixa de preço")
def books_by_price(min_price: Optional[float] = 0.0, max_price: Optional[float] = 1000.0):
    if BOOKS_DF.empty:
        return []
    filtered = BOOKS_DF[(BOOKS_DF['price'] >= min_price) & (BOOKS_DF['price'] <= max_price)]
    return filtered.to_dict(orient='records')

@app.get("/api/v1/books/{book_id}", summary="Retorna detalhes de um livro específico")
def get_book(book_id: int):
    if BOOKS_DF.empty:
        raise HTTPException(status_code=404, detail="Book not found")
        
    book = BOOKS_DF[BOOKS_DF['id'] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict(orient='records')[0]

@app.get("/api/v1/stats/overview", summary="Estatísticas gerais da coleção")
def stats_overview():
    if BOOKS_DF.empty:
        return {"total_books": 0, "average_price": 0, "rating_distribution": {}}
        
    total_books = len(BOOKS_DF)
    avg_price = round(BOOKS_DF['price'].mean(), 2)
    rating_distribution = BOOKS_DF['rating'].value_counts().to_dict()

    return {
        "total_books": total_books,
        "average_price": avg_price,
        "rating_distribution": rating_distribution
    }

@app.get("/api/v1/stats/categories", summary="Estatísticas detalhadas por categoria")
def stats_categories():
    if BOOKS_DF.empty:
        return []

    stats = BOOKS_DF.groupby('category').agg(
        book_count=('title', 'count'),
        average_price=('price', 'mean')
    ).round({'average_price': 2}).reset_index()

    return stats.to_dict(orient='records')

@app.post("/api/v1/auth/login", summary="Obtém um token de autenticação")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or not pwd_context.verify(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/auth/refresh", summary="Renova um token de autenticação")
def refresh_token(user: dict = Depends(verify_token)):
    new_token = create_access_token(data={"sub": user['sub']})
    return {"access_token": new_token, "token_type": "bearer"}

@app.get("/api/v1/scraping/trigger", summary="Dispara a execução do web scraper (protegido)")
def trigger_scraper(user: dict = Depends(verify_token)):
    try:
        python_executable = sys.executable
        script_path = "scripts/scrapping.py"
        subprocess.Popen([python_executable, script_path])
        return {"message": "Processo de scraping iniciado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao iniciar o scraper: {e}")

@app.get("/api/v1/ml/features", summary="Dados formatados para features de ML")
def ml_features():
    if BOOKS_DF.empty:
        return []
    features = BOOKS_DF[['price', 'rating', 'availability', 'category']]
    return features.to_dict(orient='records')

@app.get("/api/v1/ml/training-data", summary="Dataset pré-processado para treinamento de ML")
def ml_training_data():
    if BOOKS_DF.empty:
        return []

    df = BOOKS_DF.copy()
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map)
    df['availability_flag'] = df['availability'].apply(lambda x: 1 if 'In stock' in x else 0)
    df = df[['price', 'rating_numeric', 'availability_flag']]
    return df.to_dict(orient='records')

class BookInput(BaseModel):
    price: float
    rating_numeric: int
    availability_flag: int

@app.post("/api/v1/ml/predictions", summary="Endpoint para receber predições de um modelo de ML")
def ml_prediction(book: BookInput):
    score = (book.rating_numeric * 2) + (book.availability_flag * 1) - (book.price * 0.1)
    return {"prediction_score": round(score, 2)}