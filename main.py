#Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional
from typing import List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body


app = FastAPI()


#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=1,
        max_length=64
    )


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(defaul=None)

    
class UserRegister(User, UserLogin):
    pass
    


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(
        ...
    )
    
    
# Path Operations

## Users

###register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister=Body(...)):
    """
    Signup 
    
    This path operation register a user in the app
    
    Parameters:
        - Request body parameter
            - user: UserRegister
            
    Returns a json with the basic user information
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: datetime
        
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user
        # results = json.load(f)
        # json.dump(results, f)
        

###login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def Login():
    pass

###show all user
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass

###show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

###delete a user
@app.delete(
    path="/signup/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

#update a user
@app.put(
    path="/signup/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass

## Tweets

###show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    
)
def home():
    return {"Twitter API": "Working!!"}

###post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
def post():
    pass


### Show a tweet
@app.get(
    path="/post/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass


### Delete a tweet
@app.delete(
    path="/post/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="delete a Tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass


### Update a tweet
@app.put(
    path="/post/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="update a Tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass
