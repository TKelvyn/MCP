import asyncio
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Meuservidormcp")

@mcp.tool()
async def on_connect(event):
    print("Conectado:", event.client_id)

@mcp.tool("message")
async def handle_message(event):
    print("Mensagem:", event.data)
    await event.reply({"echo": event.data})

@mcp.tool("disconnect")
async def handle_disconnect(event):
    print("Desconectado:", event.client_id)

if __name__ == "__main__":
    mcp.run()