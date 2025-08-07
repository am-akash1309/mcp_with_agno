from agno.models.google import Gemini
from dotenv import load_dotenv  
import os

load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")

gemini_15 = Gemini(id="gemini-1.5-flash", api_key=google_api_key)
gemini_20 = Gemini(id="gemini-2.0-flash", api_key=google_api_key)
gemini_25 = Gemini(id="gemini-2.5-pro", api_key=google_api_key)

import asyncio
import gradio as gr

from agno.agent import Agent
from agno.tools.mcp import MCPTools

# MCP server URL
server_url = "http://localhost:8000/sse"


async def run_agent_once(message: str) -> str:
    # Setup and connect tool
    mcp_tools = MCPTools(transport="sse", url=server_url)
    await mcp_tools.connect()

    # Create agent
    agent = Agent(
        model=gemini_20,
        tools=[mcp_tools],
        markdown=True,
        debug_mode=True
    )

    # Run agent on message
    result = await agent.arun(message)

    # Close tool
    await mcp_tools.close()

    # Return response text
    return result.content


# Wrapper to call async function from Gradio
async def chat_interface(user_input):
    return await run_agent_once(user_input)

# Gradio UI
gr.Interface(
    fn=chat_interface,
    inputs=gr.Textbox(placeholder="Ask me something...", lines=2),
    outputs="text",
    title="MCP Agent Chat",
    description="Ask anything your agent can answer using MCP Tools.",
).launch()