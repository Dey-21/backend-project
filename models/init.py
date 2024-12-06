from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from models.sessions import Base as SessionBase
#from models.users import Base as UserBase
import os

#variable de entorno:External Database URL
datadase_url = os.getenv("DATABASE_URL") 

engine = create_engine(datadase_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#creacion tablas basadas en modelos
def initialize_database():
    pass
    #UserBase.metadata.create_all(bind=engine)
    #SessionBase.metadata.create_all(bind=engine)
