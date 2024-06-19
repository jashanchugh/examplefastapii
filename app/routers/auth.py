from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schema,models, utils,oauth2
router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: session =  Depends(database.get_db)):

    user= db.query(models.user).filter(models.user.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials") 
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credential")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":access_token,"token_type":"bearer"}
    
