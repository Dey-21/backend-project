from fastapi import FastAPI
from models import initialize_database
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

#creacion tablas
initialize_database()

if __name__ == "__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
