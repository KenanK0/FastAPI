from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
# Random = random()
# title str, content str


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


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
def get_posts():
    cursor.execute(""" SELECT * from posts """)
    posts = cursor.fetchall()

    # print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 100000)

    # my_posts.append(post_dict)

    cursor.execute(""" INSERT into posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.publish))

    res = cursor.fetchone()

    conn.commit()
    # print(res)

    return {"data": res}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # p = find_post(id)
    cursor.execute(""" Select * from posts WHERE id=%s""", (str(id)))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # index = find_index_post(id)

    cursor.execute(
        """ DELETE from posts WHERE id=%s returning * """, (str(id)))
    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)

    cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s  WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.publish, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    # post_dict = post.model_dump()
    # post_dict['id'] = id

    # my_posts[index] = post_dict
    return {"data ": post}
