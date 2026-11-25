# Reflection - Lesson 06 (MCP Gmail & Calendar)

## 1. What did we ask the agent?
We instructed the agent to build a Python MCP server (gmail-calendar) using FastMCP, uv, and stdio transport in Asia/Jerusalem, reusing OAuth credentials via GOOGLE_PRIVATE_DIR, exposing 6 read/draft/create tools, and adding .gitignore. We then listed events, created draft L06 test, scheduled MCP works 4 hours ahead, found a free slot tomorrow for Study group, and tested boundary security.

## 2. How did we check that the result is correct?
1. Verified server.py and .gitignore for exact tool signatures and zero secrets in the repository.
2. Tested via MCP ClientSession (test_server.py and run_mission.py) verifying tools/list (6 tools) and tools/call outputs.
3. Confirmed in Gmail Drafts (L06 test unsent) and Google Calendar (MCP works and Study group at 09:00-10:00).

## 3. Which tool did we leave out, and why?
We omitted send_email and delete_event to enforce Human-in-the-Loop safety: even if prompt injection appears in an email, the agent cannot send messages or delete calendar events on our behalf.

## 4. L05 vs L06: what changed?
L05 was a single hardcoded Python script for one fixed flow. L06 decouples capabilities into a reusable MCP Server exposing modular tools that any MCP client can dynamically discover and orchestrate.
