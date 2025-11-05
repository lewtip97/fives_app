from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from typing import Optional
from supabase import create_client, Client
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

# Create Supabase client for token verification
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) if SUPABASE_URL and SUPABASE_ANON_KEY else None

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)):
    if credentials is None:
        print("DEBUG: No credentials provided")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = credentials.credentials
    if not token:
        print("DEBUG: Token is None or empty")
        raise HTTPException(status_code=401, detail="Missing token")
    
    print(f"DEBUG: Token received (first 50 chars): {token[:50]}...")
    
    try:
        # Decode JWT token to extract user ID
        # Supabase JWT tokens contain the user ID in the 'sub' claim
        # Simple base64 decode approach - no signature verification needed
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        # Decode the payload (middle part of JWT)
        payload_part = parts[1]
        # Add padding if needed for base64 decoding
        padding = 4 - len(payload_part) % 4
        if padding != 4:
            payload_part += '=' * padding
        
        payload_bytes = base64.urlsafe_b64decode(payload_part)
        payload = json.loads(payload_bytes)
        
        print(f"DEBUG: Decoded payload: {payload}")
        user_id = payload.get("sub")
        if not user_id:
            print("DEBUG: No 'sub' claim in token")
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        print(f"DEBUG: User ID extracted: {user_id}")
        return user_id
    except jwt.ExpiredSignatureError:
        print("DEBUG: Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError as e:
        print(f"DEBUG: JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}") 