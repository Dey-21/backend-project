from fastapi import FastAPI
from models.init import initialize_database
import uvicorn

app = FastAPI()

#creacion tablas
initialize_database()

if __name__ == "__main__": 
    uvicorn.run("main:app", reload=True)
