from fastapi import FastAPI, Response, status, HTTPException
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
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000)

    my_posts.append(post_dict)
    print(my_posts)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    p = find_post(id)

    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    return {"data": p}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} was not found")

    post_dict = post.model_dump()
    post_dict['id'] = id

    my_posts[index] = post_dict
    return {"data ": post_dict}
