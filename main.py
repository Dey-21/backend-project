from fastapi import FastAPI
from models.init import initialize_database
import uvicorn

app = FastAPI()

#creacion tablas
initialize_database()

if __name__ == "__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
