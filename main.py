from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Random = random()
# title str, content str


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "First Post", "content": "This is the first post", "publish": True, "rating": 5, "id": 1},
            {"title": "Second Post", "content": "This is the second post", "publish": True, "rating": 4, "id": 2}]


def find_post(id):
    for item in my_posts:
        if item["id"] == id:
            return item


@app.get("/")
def root():
    return {"message": "Kenan Kasongo blabla"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000)

    my_posts.append(post_dict)
    print(my_posts)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id:int):
    p = find_post(id)

    return {"data": p}
