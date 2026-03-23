from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import os
import httpx
from dotenv import load_dotenv
import base64

load_dotenv()

app = FastAPI()

user_tokens = {}

FIGMA_CLIENT_ID = os.getenv("FIGMA_CLIENT_ID")
FIGMA_CLIENT_SECRET = os.getenv("FIGMA_CLIENT_SECRET")
FIGMA_REDIRECT_URI = os.getenv("FIGMA_REDIRECT_URI")

@app.get("/")
def get_root():
    return {"message": "Hello FastAPI"}

@app.get("/login")
def login():
    figma_oauth_url = (
        "https://www.figma.com/oauth?"
        f"client_id={FIGMA_CLIENT_ID}"
        f"&redirect_uri={FIGMA_REDIRECT_URI}"
        f"&scope=file_read"
        f"&response_type=code"
    )
    return RedirectResponse(figma_oauth_url)

@app.get("/callback")
async def callback(code: str):
    try:
        credentials = f"{FIGMA_CLIENT_ID}:{FIGMA_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode().decode())

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "applications/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": FIGMA_REDIRECT_URI
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.figma.com/v1/oauth/token",
                headers=headers,
                data=data
            )
        
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=res.text)
        
        token_data = res.json()

        user_tokens['demo_user'] = token_data

        return {
            "message": "Login success",
            "token": token_data
        }
    
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e)) 


