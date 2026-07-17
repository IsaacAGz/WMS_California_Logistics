"""Invoke Canvas Authoring MCP sync_canvas via stdio."""
import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ENV_ID = "Default-47c551c6-5fb2-480e-939a-c8e6c57d73ba"
APP_ID = "9619f3e7-a136-42ed-8a99-d0463f8d6905"
LOGIN_HINT = "revisor@californialg.onmicrosoft.com"
TARGET_DIR = r"C:\Users\PC\Documents\Code\WMS_California_Logistics\wms-california-logistics-v2"


async def main() -> int:
    server_params = StdioServerParameters(
        command="cmd",
        args=[
            "/c",
            r"C:\Program Files\dotnet\dnx.cmd",
            "Microsoft.PowerApps.CanvasAuthoring.McpServer",
            "--yes",
            "--prerelease",
            "--source",
            "https://api.nuget.org/v3/index.json",
        ],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            connect_result = await session.call_tool(
                "connect",
                {
                    "environment_id": ENV_ID,
                    "app_id": APP_ID,
                    "login_hint": LOGIN_HINT,
                },
            )
            print("CONNECT:", connect_result.content)

            sync_result = await session.call_tool(
                "sync_canvas",
                {"directoryPath": TARGET_DIR},
            )
            print("SYNC:", sync_result.content)

            if sync_result.isError:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
