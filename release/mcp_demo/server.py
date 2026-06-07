"""简易 MCP Server 示例。

通过 stdio 传输暴露工具、资源和提示词，供 MCP Client 调用。
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """将两个整数相加。"""
    return a + b


@mcp.tool()
def echo(message: str) -> str:
    """原样返回输入的消息。"""
    return message


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """返回个性化问候语。"""
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """生成问候提示词。"""
    styles = {
        "friendly": "请写一段温暖、友好的问候语",
        "formal": "请写一段正式、专业的问候语",
        "casual": "请写一段轻松、随意的问候语",
    }
    return f"{styles.get(style, styles['friendly'])}，对象是 {name}。"


if __name__ == "__main__":
    mcp.run(transport="stdio")
