import asyncio, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="uv", args=["run", "server.py"], env=dict(os.environ))
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            print("tools/list ->", [t.name for t in (await s.list_tools()).tools])
            res = await s.call_tool("list_events", {"days_ahead": 1})
            print("tools/call ->", res.content[0].text)

asyncio.run(main())
