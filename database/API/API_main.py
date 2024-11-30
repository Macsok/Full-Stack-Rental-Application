from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int


class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    return post


@app.get("/posts_vulnerable/{post_title}", status_code=status.HTTP_200_OK)
async def read_post(post_title: str, db: db_dependency):
    # Example of SQL Injection:
    # If post_title is "' OR '1'='1", the query becomes:
    # SELECT * FROM posts WHERE title = '' OR '1'='1'
    # This will return all rows in the posts table.
    # http://localhost:8000/posts_vulnerable/%27%20OR%20%271%27%3D%271
    posts = db.execute(text(f"SELECT * FROM posts WHERE title = '{post_title}'")).fetchall()
    if not posts:
        raise HTTPException(status_code=404, detail='Post was not found')
    return [dict(post._mapping) for post in posts]


@app.delete("/posts", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user