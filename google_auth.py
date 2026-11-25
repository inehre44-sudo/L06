import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
]

def get_credentials() -> Credentials:
    private_dir = os.environ.get("GOOGLE_PRIVATE_DIR")
    if not private_dir:
        raise RuntimeError("GOOGLE_PRIVATE_DIR environment variable is not set.")
    
    token_path = Path(private_dir) / "token.json"
    if not token_path.exists():
        raise FileNotFoundError(f"token.json not found in {private_dir}")

    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds

def get_services():
    creds = get_credentials()
    gmail = build("gmail", "v1", credentials=creds)
    calendar = build("calendar", "v3", credentials=creds)
    return gmail, calendar
