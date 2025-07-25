import os

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()
app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-that-never-changes",
    max_age=3600,
    same_site="lax",
    https_only=False, 
)
oauth = OAuth()
oauth.register(
    name="linkedin",
    client_id=os.getenv("LINKEDIN_CLIENT_ID"),
    client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
    authorize_url="https://www.linkedin.com/oauth/v2/authorization",
    access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
    api_base_url="https://api.linkedin.com/v2/",
    client_kwargs={"scope": "openid email profile"},
)
linkedin = oauth.create_client("linkedin")


@app.get("/auth/login")
async def login(request: Request):
    print(f"Session before OAuth: {request.session}")
    redirect_uri = request.url_for("auth_callback")
    response = await oauth.linkedin.authorize_redirect(request, redirect_uri)
    print(f"Session after OAuth: {request.session}")
    return response


@app.get("/auth/callback")
async def auth_callback(request: Request):
    print(f"Session in callback: {request.session}")
    print(f"URL params: {dict(request.query_params)}")

    try:
        token = await oauth.linkedin.authorize_access_token(request)
        return {"success": True, "token": token}
    except Exception as e:
        print(f"OAuth error: {e}")
        return {"error": str(e), "session": dict(request.session)}
