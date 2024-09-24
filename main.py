from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


BASE_URL = "https://jsonplaceholder.typicode.com"


async def fetch_data(endpoint: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()


@app.get("/posts")
async def get_posts():
    try:
        data = await fetch_data("/posts")
        return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error fetching posts")


@app.get("/users")
async def get_users():
    try:
        data = await fetch_data("/users")
        return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error fetching users")


@app.post("/posts")
async def create_post(post: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/posts", json=post)
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error creating post")


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/posts/{post_id}", json=post)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error updating post")


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/posts/{post_id}")
        if response.status_code == 200:
            return {"detail": "Post deleted successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error deleting post")