# L06 - Gmail & Calendar MCP Server (gmail-calendar)

Local MCP server built with FastMCP, uv, and stdio transport in Asia/Jerusalem timezone, reusing OAuth credentials from GOOGLE_PRIVATE_DIR.

## Tools (6)
1. search_emails(query, max_results)
2. read_email(message_id)
3. create_draft(to, subject, body)
4. list_events(days_ahead)
5. find_free_slots(date, duration_minutes)
6. create_event(title, start, end, description)

## Run
Set GOOGLE_PRIVATE_DIR, run uv sync, then run uv run python test_server.py and uv run python run_mission.py.
