from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# get_db()
# Random = random()
# title str, content str


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host="localhost", database='fastapi',
                                user='postgres', password='kenan', cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        print("DB connection hasss succcesssfullyy")
        break

    except Exception as error:
        print("Connexion Failed")
        print("Error", error)
        time.sleep(2)


my_posts = [{"title": "First Post", "content": "This is the first post", "publish": True, "rating": 5, "id": 1},
            {"title": "Second Post", "content": "This is the second post", "publish": True, "rating": 4, "id": 2}]


def find_post(id):
    for item in my_posts:
        if item["id"] == id:
            return item


# def delete_post(id):
#     post = find_post(id)
#     if not post:
#         return False
#     my_posts.remove(post)

#     return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Kenan Kasongo blabla"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 100000)

    # my_posts.append(post_dict)

    # cursor.execute(""" INSERT into posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.publish))

    # res = cursor.fetchone()

    # conn.commit()
    # print(res)

    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # p = find_post(id)
    # cursor.execute(""" Select * from posts WHERE id=%s""", (str(id)))

    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # index = find_index_post(id)

    # cursor.execute(
    #     """ DELETE from posts WHERE id=%s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # index = find_index_post(id)

    # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s  WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.publish, str(id)))
    # post = cursor.fetchone()
    # conn.commit()


    post_query= db.query(models.Post).filter(models.Post.id == id)
    post_to_delete= post_query.first()

    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with the id {id} was not found")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    # post_dict = post.model_dump()
    # post_dict['id'] = id

    # my_posts[index] = post_dict
    return {"data ": post_query.first()}
