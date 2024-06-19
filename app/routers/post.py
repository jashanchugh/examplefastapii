
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schema,oauth2
from ..database import get_db
from sqlalchemy.orm import session
from typing import List,Optional
from sqlalchemy import func




router = APIRouter(
    prefix="/posts" ,
    tags=['Posts']
)


@router.get("/",response_model=List[schema.PostOut])
def get_posts(db: session= Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit : int = 5,skip: int = 0,search : Optional[str]= ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts =cursor.fetchall()
    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

@router.post("/",response_model=schema.Post)
# def create_posts(post: Post):
def create_posts(post:schema.PostCreate,db:session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # print(**post.dict()) UNPACKING DICTIONARY
    # new_post =models.Post(title=post.title,content=post.content,published=post.published)
  
    new_post =models.Post(owner_id = current_user.id,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *"""
    #                ,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post
@router.get("/{id}",response_model=schema.PostOut)
def get_post(id: int, response : Response,db:session = Depends(get_db),currennt_user : int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message':f"post with {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found" )
    return post  

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # # index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f"post the id: {id} does not exist " )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized To Perform Requested Action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(deleted_post)
    return{"message":"the post was successfully deletd"}

@router.put("/{id}",response_model=schema.Post)
def update_post(id: int,updated_post: schema.PostCreate,db:session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()

    # cursor.execute("""update posts set title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.published,str(id)))
    # updated_post  = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f"post the id: {id} does not exist " )
    
     
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized To Perform Requested Action")
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first() 