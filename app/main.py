from fastapi import FastAPI
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional,List
# from random import randrange
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
# from sqlalchemy.orm import session
from .routers import post,user,auth,vote
from .config import settings

from dotenv import load_dotenv
import os
import uvicorn



app = FastAPI()

origins = ["*"]


load_dotenv()

PORT = int(os.get('PORT', 8000))
HOST = '0.0.0.0'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# def get_db():
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# models.Base.metadata.create_all(bind=engine)


# @app.get("/sqlalchemy")
# def test_posts(db:session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"data":posts}
#     # return {"status":"success"}



# def find_posts(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i , p in enumerate(my_posts):
#         if p['id'] == id:   
#             return i



if __name__ == '__main__':
    uvicorn.run('app.main:app', host = HOST, port = PORT, reload = True)
 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message":"hello world????"}


