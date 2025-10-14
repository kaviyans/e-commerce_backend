from fastapi import FastAPI
from app.api.routers import products


app = FastAPI(title="E-commerce Backend API")


app.include_router(products.router, prefix="/products", tags=["Products"])


@app.get("/")
def root():
    return {"message": "E-commerce API is running 🚀"}