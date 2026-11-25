import asyncio, os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TZ = ZoneInfo("Asia/Jerusalem")

async def main():
    params = StdioServerParameters(command="uv", args=["run", "server.py"], env=dict(os.environ))
    async with stdio_client(params) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            tools = [t.name for t in (await s.list_tools()).tools]
            print("=== Step 5 & 8: MCP Tools ===\n", tools)            
            print("\n=== Step 8: List tomorrow's events ===")
            print((await s.call_tool("list_events", {"days_ahead": 1})).content[0].text)
            print("\n\n=== Step 9: L05 Mission via MCP ===")
            d = await s.call_tool("create_draft", {"to": "me", "subject": "L06 test", "body": "Testing MCP server from L06!"})
            print(d.content[0].text)
            now = datetime.now(TZ)
            s4h = (now + timedelta(hours=4)).replace(second=0, microsecond=0)
            e4h = s4h + timedelta(hours=1)
            ev = await s.call_tool("create_event", {"title": "MCP works", "start": s4h.isoformat(), "end": e4h.isoformat(), "description": "Created via MCP"})
            print(ev.content[0].text)
            print("\n=== Step 10: Find free slot & schedule Study group ===")
            tom = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            slots = (await s.call_tool("find_free_slots", {"date": tom, "duration_minutes": 60})).content[0].text
            print("Free slots tomorrow:", slots)
            f1 = slots.split(",")[0].strip().split("-")[0]
            sg_s = f"{tom}T{f1}:00"
            sg_e = (datetime.fromisoformat(sg_s) + timedelta(hours=1)).isoformat()
            sg = await s.call_tool("create_event", {"title": "Study group", "start": sg_s, "end": sg_e})
            print(sg.content[0].text)
            print("\n=== Step 11: Security Boundary Check ===")
            print("Send tool exposed:", any("send" in t for t in tools))
            print("Delete tool exposed:", any("delete" in t for t in tools))

asyncio.run(main())
