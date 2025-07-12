# api/main.py

from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from api.auth import create_access_token, verify_token, fake_user, pwd_context
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Books API", version="1.0")

BOOKS_DF = pd.read_csv('data/books.csv')

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/books")
def list_books():
    return BOOKS_DF.to_dict(orient='records')

@app.get("/api/v1/books/{book_id}")
def get_book(book_id: int):
    book = BOOKS_DF[BOOKS_DF['id'] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict(orient='records')[0]

@app.get("/api/v1/categories")
def list_categories():
    categories = BOOKS_DF['category'].dropna().unique().tolist()
    return {"categories": categories}

@app.get("/api/v1/books/search")
def search_books(title: str = None, category: str = None):
    df = BOOKS_DF
    if title:
        df = df[df['title'].str.contains(title, case=False, na=False)]
    if category:
        df = df[df['category'].str.contains(category, case=False, na=False)]
    return df.to_dict(orient='records')

# Overview geral: total de livros, preço médio, ratings
@app.get("/api/v1/stats/overview")
def stats_overview():
    total_books = len(BOOKS_DF)
    avg_price = round(BOOKS_DF['price'].mean(), 2)
    rating_distribution = BOOKS_DF['rating'].value_counts().to_dict()

    return {
        "total_books": total_books,
        "average_price": avg_price,
        "rating_distribution": rating_distribution
    }

# Estatísticas por categoria
@app.get("/api/v1/stats/categories")
def stats_categories():
    stats = BOOKS_DF.groupby('category').agg({
        'title': 'count',
        'price': 'mean'
    }).rename(columns={'title': 'book_count', 'price': 'average_price'}).reset_index()

    return stats.to_dict(orient='records')

# Top livros com melhor rating (mockado pela frequência do rating)
@app.get("/api/v1/books/top-rated")
def top_rated_books():
    top_books = BOOKS_DF[BOOKS_DF['rating'] == 'Five'].head(10)
    return top_books.to_dict(orient='records')

# Livros por faixa de preço
@app.get("/api/v1/books/price-range")
def books_by_price(min: Optional[float] = 0.0, max: Optional[float] = 100.0):
    filtered = BOOKS_DF[(BOOKS_DF['price'] >= min) & (BOOKS_DF['price'] <= max)]
    return filtered.to_dict(orient='records')

@app.post("/api/v1/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or not pwd_context.verify(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/auth/refresh")
def refresh_token(user: dict = Depends(verify_token)):
    new_token = create_access_token(data={"sub": user['sub']})
    return {"access_token": new_token, "token_type": "bearer"}

@app.get("/api/v1/scraping/trigger")
def trigger_scraper(user: dict = Depends(verify_token)):
    return {"message": "Scraper executado com sucesso"}

@app.get("/api/v1/ml/features")
def ml_features():
    features = BOOKS_DF[['price', 'rating', 'availability', 'category']]
    return features.to_dict(orient='records')

@app.get("/api/v1/ml/training-data")
def ml_training_data():
    df = BOOKS_DF.copy()
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map)
    df['availability_flag'] = df['availability'].apply(lambda x: 1 if 'In stock' in x else 0)
    df = df[['price', 'rating_numeric', 'availability_flag']]
    return df.to_dict(orient='records')

from pydantic import BaseModel

class BookInput(BaseModel):
    price: float
    rating_numeric: int
    availability_flag: int

@app.post("/api/v1/ml/predictions")
def ml_prediction(book: BookInput):
    # Mock de um modelo simples: quanto maior rating e disponibilidade, maior chance de ser popular
    score = (book.rating_numeric * 2) + (book.availability_flag * 1) - (book.price * 0.1)
    return {"prediction_score": round(score, 2)}
