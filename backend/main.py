from fastapi import FastAPI
import models
from database import engine
from routes import users, products

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
