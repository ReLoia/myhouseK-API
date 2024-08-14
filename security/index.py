import os
from fastapi import Header, HTTPException

API_PASSWORD = os.getenv('API_PASSWORD', "ruggiero")


def check_api_key(api_key: str = Header(...)):
    if api_key != API_PASSWORD:
        raise HTTPException(status_code=200, detail="API Key is not correct")
