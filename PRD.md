# Product Requirements Document (PRD) - Gmail & Calendar MCP Server (L06)

## 1. Overview & Objective
Build a local Model Context Protocol (MCP) server in Python (gmail-calendar) using FastMCP and stdio transport that allows an LLM client to securely interact with Gmail and Google Calendar in the Asia/Jerusalem timezone.

## 2. Core Functional Requirements
- Gmail Read & Search: Search messages (search_emails) and read message content/metadata (read_email).
- Gmail Draft Creation: Create unsent email drafts (create_draft) without automatic sending.
- Calendar Read & Availability: List upcoming calendar events (list_events) and calculate free time slots (find_free_slots).
- Calendar Event Scheduling: Create new events (create_event) with timezone-aware ISO timestamps.

## 3. Security & Non-Functional Requirements
- Human-in-the-Loop Safety: Destructive or irreversible actions (send_email, delete_event) are intentionally omitted to mitigate prompt injection risks.
- Credential Isolation: OAuth credentials (credentials.json, token.json) are stored outside the repository via GOOGLE_PRIVATE_DIR and excluded in .gitignore.
- Verification: Automated end-to-end validation via MCP ClientSession (test_server.py, run_mission.py).
