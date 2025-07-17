from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL")
SUPABASE_JWT_ALG = "ES256"


bearer_scheme = HTTPBearer()

def get_jwk_for_kid(kid):
    resp = requests.get(
        SUPABASE_JWKS_URL,
        headers={"apikey": SUPABASE_ANON_KEY}
    )
    print("JWKS status code:", resp.status_code)
    print("JWKS response text:", resp.text)
    jwks = resp.json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    raise Exception("Public key not found for kid: " + kid)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    headers = jwt.get_unverified_header(token)
    jwk = get_jwk_for_kid(headers["kid"])
    try:
        payload = jwt.decode(
            token,
            jwk,
            algorithms=[SUPABASE_JWT_ALG],
            options={"verify_aud": False}
        )
        return payload["sub"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") 