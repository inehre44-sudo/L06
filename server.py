import base64
from datetime import datetime, timedelta
from email.message import EmailMessage
from zoneinfo import ZoneInfo
from mcp.server.fastmcp import FastMCP
from google_auth import get_services

mcp = FastMCP("gmail-calendar")
TZ = ZoneInfo("Asia/Jerusalem")

@mcp.tool()
def search_emails(query: str, max_results: int = 5) -> str:
    """Search Gmail messages matching a query string (e.g., sender, subject, keyword). Does NOT modify or send emails."""
    gmail, _ = get_services()
    res = gmail.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = res.get("messages", [])
    if not messages:
        return "No matching emails found."
    out = []
    for m in messages:
        msg = gmail.users().messages().get(userId="me", id=m["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"]).execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        out.append(f"ID: {m['id']} | From: {headers.get('From','')} | Subject: {headers.get('Subject','')} | Date: {headers.get('Date','')}")
    return "\n".join(out)

@mcp.tool()
def read_email(message_id: str) -> str:
    """Read the snippet and headers of a single Gmail message by its message_id. Read-only."""
    gmail, _ = get_services()
    msg = gmail.users().messages().get(userId="me", id=message_id, format="full").execute()
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return f"From: {headers.get('From','')}\nSubject: {headers.get('Subject','')}\nDate: {headers.get('Date','')}\nSnippet: {msg.get('snippet','')}"

@mcp.tool()
def create_draft(to: str, subject: str, body: str) -> str:
    """Create a Gmail DRAFT only. Does NOT send the email. Use 'me' as 'to' to draft to the user's own address."""
    gmail, _ = get_services()
    if to.strip().lower() == "me":
        profile = gmail.users().getProfile(userId="me").execute()
        to = profile["emailAddress"]
    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["Subject"] = subject
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = gmail.users().drafts().create(userId="me", body={"message": {"raw": encoded}}).execute()
    return f"Draft created successfully (id: {draft['id']}) to {to} with subject '{subject}'."

@mcp.tool()
def list_events(days_ahead: int = 1) -> str:
    """List upcoming Google Calendar events for the next days_ahead days in Asia/Jerusalem time zone."""
    _, calendar = get_services()
    now = datetime.now(TZ)
    end = now + timedelta(days=days_ahead)
    events_res = calendar.events().list(
        calendarId="primary", timeMin=now.isoformat(), timeMax=end.isoformat(), singleEvents=True, orderBy="startTime"
    ).execute()
    events = events_res.get("items", [])
    if not events:
        return "No upcoming events found."
    lines = []
    for e in events:
        start = e["start"].get("dateTime", e["start"].get("date"))
        lines.append(f"- {start}: {e.get('summary', '(No title)')}")
    return "\n".join(lines)

@mcp.tool()
def find_free_slots(date: str, duration_minutes: int = 60) -> str:
    """Find free slots on a given date (YYYY-MM-DD) between 09:00 and 17:00 Asia/Jerusalem time."""
    _, calendar = get_services()
    day_start = datetime.fromisoformat(f"{date}T09:00:00").replace(tzinfo=TZ)
    day_end = datetime.fromisoformat(f"{date}T17:00:00").replace(tzinfo=TZ)
    body = {"timeMin": day_start.isoformat(), "timeMax": day_end.isoformat(), "timeZone": "Asia/Jerusalem", "items": [{"id": "primary"}]}
    busy = calendar.freebusy().query(body=body).execute()["calendars"]["primary"]["busy"]
    slots = []
    cursor = day_start
    delta = timedelta(minutes=duration_minutes)
    for b in busy:
        b_start = datetime.fromisoformat(b["start"]).astimezone(TZ)
        b_end = datetime.fromisoformat(b["end"]).astimezone(TZ)
        while cursor + delta <= b_start:
            slots.append(f"{cursor.strftime('%H:%M')}-{(cursor+delta).strftime('%H:%M')}")
            cursor += delta
        if b_end > cursor:
            cursor = b_end
    while cursor + delta <= day_end:
        slots.append(f"{cursor.strftime('%H:%M')}-{(cursor+delta).strftime('%H:%M')}")
        cursor += delta
    return ", ".join(slots) if slots else "No free slots found."

@mcp.tool()
def create_event(title: str, start: str, end: str, description: str = "") -> str:
    """Create a new Google Calendar event. start and end must be ISO strings (e.g., '2026-11-25T18:30:00'). Does NOT delete events."""
    _, calendar = get_services()
    if "+" not in start and not start.endswith("Z"):
        start = datetime.fromisoformat(start).replace(tzinfo=TZ).isoformat()
    if "+" not in end and not end.endswith("Z"):
        end = datetime.fromisoformat(end).replace(tzinfo=TZ).isoformat()
    event_body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start, "timeZone": "Asia/Jerusalem"},
        "end": {"dateTime": end, "timeZone": "Asia/Jerusalem"},
    }
    created = calendar.events().insert(calendarId="primary", body=event_body).execute()
    return f"Event '{title}' created from {start} to {end} (id: {created['id']})."

if __name__ == "__main__":
    mcp.run(transport="stdio")
