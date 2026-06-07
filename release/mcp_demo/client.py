"""简易 MCP Client 示例。

启动 server.py 子进程，通过 stdio 连接并演示 MCP 协议交互。
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl

SERVER_SCRIPT = Path(__file__).resolve().parent / "server.py"


async def run() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )

    print("正在连接 MCP Server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("连接成功，已完成 initialize 握手\n")

            tools = await session.list_tools()
            print(f"可用工具: {[t.name for t in tools.tools]}")

            resources = await session.list_resources()
            print(f"可用资源: {[r.uri for r in resources.resources]}")

            prompts = await session.list_prompts()
            print(f"可用提示词: {[p.name for p in prompts.prompts]}\n")

            resource_content = await session.read_resource(AnyUrl("greeting://World"))
            resource_block = resource_content.contents[0]
            if hasattr(resource_block, "text"):
                print(f"读取资源 greeting://World -> {resource_block.text}")

            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            add_block = result.content[0]
            if isinstance(add_block, types.TextContent):
                print(f"调用工具 add(5, 3) -> {add_block.text}")

            echo_result = await session.call_tool("echo", arguments={"message": "MCP demo works!"})
            echo_block = echo_result.content[0]
            if isinstance(echo_block, types.TextContent):
                print(f"调用工具 echo(...) -> {echo_block.text}")

            if prompts.prompts:
                prompt = await session.get_prompt(
                    "greet_user",
                    arguments={"name": "Alice", "style": "friendly"},
                )
                prompt_text = prompt.messages[0].content
                if isinstance(prompt_text, types.TextContent):
                    print(f"获取提示词 greet_user -> {prompt_text.text}")

    print("\nMCP Client 演示完成。")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
