from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import os
import httpx
from dotenv import load_dotenv
import base64
from starlette.middleware.sessions import SessionMiddleware
import secrets
import urllib.parse

load_dotenv()

app = FastAPI()

user_tokens = {}

FIGMA_CLIENT_ID = os.getenv("FIGMA_CLIENT_ID")
FIGMA_CLIENT_SECRET = os.getenv("FIGMA_CLIENT_SECRET")
FIGMA_REDIRECT_URI = os.getenv("FIGMA_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

@app.get("/")
def get_root():
    return {"message": "Hello FastAPI"}

@app.get("/login")
def login(request: Request):

    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    redirect_uri = urllib.parse.quote(FIGMA_REDIRECT_URI, safe="")

    scope = "file_content:read file_metadata:read"

    figma_oauth_url = (
        "https://www.figma.com/oauth?"
        f"client_id={FIGMA_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={urllib.parse.quote(scope)}"
        f"&response_type=code"
        f"&state={state}"
    )
    return RedirectResponse(figma_oauth_url)

@app.get("/callback")
async def callback(request: Request, code: str, state: str = None):
    try:
        if state != request.session.get("oauth_state"):
            raise HTTPException(status_code=400, detail="Invalid state")
        
        credentials = f"{FIGMA_CLIENT_ID}:{FIGMA_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
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


